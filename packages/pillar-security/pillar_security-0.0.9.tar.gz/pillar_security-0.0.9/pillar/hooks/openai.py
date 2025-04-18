import uuid
import traceback
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion
    from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from typing import TYPE_CHECKING, Iterable
from .. import context_vars

if TYPE_CHECKING:
    from ..pillar import Pillar

SERVICE_NAME = 'openai'


def chunking_handler(pillar, iter: Iterable['ChatCompletionChunk'], session_id, model):
    message = ''
    function_name = ''
    function_arguments = ''
    new_tools = {}

    for chunk in iter:
        try:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content is not None:
                message += delta.content

            function_call = delta.function_call if hasattr(delta, 'function_call') else None
            if function_call is not None:
                if function_call.name is not None:
                    function_name += function_call.name
                if function_call.arguments is not None:
                    function_arguments += function_call.arguments

            tools = delta.tool_calls if hasattr(delta, 'tool_calls') else None
            if tools is not None:
                for tool in tools:
                    function_call = tool.function
                    if tool.index not in new_tools:
                        new_tools[tool.index] = {'name': '', 'arguments': ''}
                    if function_call.name is not None:
                        new_tools[tool.index]['name'] += function_call.name
                    if function_call.arguments is not None:
                        new_tools[tool.index]['arguments'] += function_call.arguments
        except Exception:
            pillar.logger.error('Exception in openai.chat.completions.create hook')
            pillar.logger.error(traceback.format_exc())
        finally:
            yield chunk

    if message:
        pillar._write(session_id, message, 'assistant', 'assistant', model, SERVICE_NAME)
    if function_name:
        pillar._write(
            session_id,
            f'[tool call] {function_name}({function_arguments})',
            'assistant',
            'assistant',
            model,
            SERVICE_NAME)

    for tool in new_tools.values():
        pillar._write(
            session_id,
            f'[tool call] {tool["name"]}({tool["arguments"]})',
            'assistant',
            'assistant',
            model,
            SERVICE_NAME)


def hook_chat_completions(pillar: 'Pillar'):
    def hook(wrapped, instance, args, kwargs):
        try:
            if len(args) > 0:
                pillar.logger.error('Expected openai.chat.completions.create to be called with keyword arguments only')
                return wrapped(*args, **kwargs)

            if 'messages' not in kwargs:
                pillar.logger.error('Expected openai.chat.completions.create to be called with keyword argument messages')
                return wrapped(*args, **kwargs)

            if 'model' not in kwargs:
                pillar.logger.error('Expected openai.chat.completions.create to be called with keyword argument model')
                return wrapped(*args, **kwargs)

            messages = kwargs['messages']
            model = kwargs['model']

            if 'functions' in kwargs:
                for function in kwargs['functions']:
                    pillar._write_tool(function['name'], function['description'], function['parameters'])

            if 'tools' in kwargs:
                for tool in kwargs['tools']:
                    if tool['type'] == 'function':
                        function = tool['function']
                        pillar._write_tool(function['name'], function['description'], function['parameters'])

            session_id = context_vars.session_id.get()
            if session_id is None:
                session_id = str(uuid.uuid4())

            if len(messages) > 0 and messages[0]['role'] == 'system':
                pillar._write(
                    session_id,
                    messages[0]['content'],
                    messages[0]['role'],
                    messages[0]['role'],
                    model,
                    SERVICE_NAME)

            if len(messages) > 0 and messages[-1]['role'] != 'system':
                user_id = context_vars.user_id.get()
                if user_id is None:
                    user_id = kwargs.get('user', '')
                role = messages[-1]['role'] if messages[-1]['role'] != 'tool' else 'function'
                initiator = user_id if messages[-1]['role'] == 'user' else role
                pillar._write(session_id, messages[-1]['content'], role, initiator, model, SERVICE_NAME)

            result: 'ChatCompletion' = wrapped(*args, **kwargs)

            if kwargs.get('stream', False):
                return chunking_handler(pillar, result, session_id, model)

            message = result.choices[0].message
            if message.content is not None:
                pillar._write(session_id, message.content, message.role, message.role, model, SERVICE_NAME)

            if hasattr(message, 'function_call') and message.function_call is not None:
                function_call = message.function_call
                pillar._write(
                    session_id,
                    f'[function call] {function_call.name}({function_call.arguments})',
                    message.role,
                    message.role,
                    model,
                    SERVICE_NAME)

            if hasattr(message, 'tool_calls') and message.tool_calls is not None:
                for tool in message.tool_calls:
                    if tool.type == 'function':
                        function_call = tool.function
                        pillar._write(
                            session_id,
                            f'[function call] {function_call.name}({function_call.arguments})',
                            message.role,
                            message.role,
                            model,
                            SERVICE_NAME)

            return result
        except Exception:
            pillar.logger.error('Exception in openai.chat.completions.create hook')
            pillar.logger.error(traceback.format_exc())
            return wrapped(*args, **kwargs)

    return hook
