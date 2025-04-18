import requests
import datetime
import importlib.metadata
import uuid
import logging
from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Optional
from contextlib import contextmanager
from packaging import version
from wrapt import wrap_function_wrapper

from .logging import Logger
from .hooks.openai import hook_chat_completions
from . import context_vars


@dataclass
class Report:
    block: bool


def _uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


class Pillar:
    _instance = None

    def __init__(self, url, app_id, api_key):
        if not _uri_validator(url):
            raise ValueError(f'Invalid url for pillar: {url}')
        self.url = url
        self.app_id = app_id
        self.api_key = api_key
        self.requests = requests.Session()
        self.requests.headers.update({
            'X-App-Id': app_id,
            'X-Api-Key': api_key,
        })
        self.logger = Logger(self)

        if Pillar._instance is not None:
            logging.warning(
                'Pillar was initialized more than once. If using streamlit, use st.cache_resource to cache the Pillar object.')
        else:
            Pillar._instance = self  # This also prevents the instance from being garbage collected
            self._initialize_hooks()

    def check_prompt(self, prompt: str, policy: str = 'default') -> Report:
        return self._check_prompt(prompt, policy)

    def _check_prompt(self, prompt: str, policy: str = 'default', role: str = 'user'):
        url = f'{self.url}/application/check_prompt'
        if context_vars.app_id.get() and context_vars.api_key.get():
            self.requests.headers.update({
                'X-App-Id': context_vars.app_id.get(),
                'X-Api-Key': context_vars.api_key.get(),
            })
        response = self.requests.post(url, json={            
            'session_id': context_vars.session_id.get() or str(uuid.uuid4()),
            'message': prompt,
            'policy': policy,
            'initiator': context_vars.user_id.get() or '',
            'role': role,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        if response.status_code != 200:
            raise RuntimeError(f'Unexpected status code {response.status_code} from pillar guard. {response.text}')

        return Report(block=response.json()['action'] == 'block')

    def check_response(self, response: str, policy: str = 'default'):
        url = f'{self.url}/application/check_response'
        message_id = context_vars.last_assistant_message_id.get()
        if context_vars.app_id.get() and context_vars.api_key.get():
            self.requests.headers.update({
                'X-App-Id': context_vars.app_id.get(),
                'X-Api-Key': context_vars.api_key.get(),
            })
        response = self.requests.post(url, json={  
            'id': message_id,
            'session_id': context_vars.session_id.get() or str(uuid.uuid4()),
            'message': response,
            'policy': policy,
            'initiator': 'assistant',
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        if response.status_code != 200:
            raise RuntimeError(f'Unexpected status code {response.status_code} from pillar guard. {response.text}')
        return Report(block=response.json()['action'] == 'block')

    def check_tool_response(self, response: str, policy: str = 'default'):
        return self._check_prompt(response, policy, role='function')

    def _write(self, session_id: str, message: str, role: str, initiator: str, model: str, service: str):
        url = f'{self.url}/application/messages'
        message_id = str(uuid.uuid4())
        if context_vars.app_id.get() and context_vars.api_key.get():
            self.requests.headers.update({
                'X-App-Id': context_vars.app_id.get(),
                'X-Api-Key': context_vars.api_key.get(),
            })
        if role == 'assistant':
            context_vars.last_assistant_message_id.set(message_id)
        self.requests.post(url, json={
            'id': message_id,
            'message': message,
            'role': role,
            'initiator': initiator,
            'model': model,
            'service': service,
            'session_id': session_id,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })

    def _write_tool(self, name: str, description: str, parameters: dict):
        url = f'{self.url}/application/tools'
        if context_vars.app_id.get() and context_vars.api_key.get():
            self.requests.headers.update({
                'X-App-Id': context_vars.app_id.get(),
                'X-Api-Key': context_vars.api_key.get(),
            })
        self.requests.post(url, json={
            'name': name,
            'description': description,
            'parameters': parameters,
        })

    def _log(self, level, message):
        url = f'{self.url}/application/logs'
        if context_vars.app_id.get() and context_vars.api_key.get():
            self.requests.headers.update({
                'X-App-Id': context_vars.app_id.get(),
                'X-Api-Key': context_vars.api_key.get(),
            })
        try:
            self.requests.post(url, json={
                'level': level,
                'message': message,
                'timestamp': datetime.datetime.utcnow().isoformat()
            })
        except Exception:
            logging.log(level, message)

    @contextmanager
    def session(self, user_id: Optional[str] = None, session_id: Optional[str] = None):
        if session_id is None:
            session_id = str(uuid.uuid4())

        session_id_token = context_vars.session_id.set(session_id)
        token_user_id = context_vars.user_id.set(user_id)
        try:
            yield
        finally:
            context_vars.session_id.reset(session_id_token)
            context_vars.user_id.reset(token_user_id)
    
    @contextmanager
    def app_credentials(self, app_id: str, api_key: str):
        app_id_token = context_vars.app_id.set(app_id)
        api_key_id = context_vars.api_key.set(api_key)
        try:
            yield
        finally:
            context_vars.app_id.reset(app_id_token)
            context_vars.api_key.reset(api_key_id)

    def _initialize_hooks(self):
        self._initialize_hooks_openai()

    def _initialize_hooks_openai(self):
        try:
            openai_version = version.parse(importlib.metadata.version('openai'))
        except importlib.metadata.PackageNotFoundError:
            return

        if openai_version < version.parse('1.0.0'):
            wrap_function_wrapper('openai', 'ChatCompletion.create', hook_chat_completions(self))
        else:
            wrap_function_wrapper('openai.resources.chat.completions', 'Completions.create', hook_chat_completions(self))
