from pytest import fixture
from unittest.mock import patch, ANY

import openai as openai_
from pillar import Pillar


@fixture(scope='session')
def mock_requests_post():
    with patch('requests.sessions.Session.post') as mock_post:
        yield mock_post


@fixture(scope='session')
def pillar(mock_requests_post):
    return Pillar(url='http://localhost:8000', app_id='test', api_key='test')


@fixture(scope='session')
def openai():
    return openai_.Client()


def test_oneline_installation(pillar, openai, mock_requests_post):
    openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello.'},
        ]
    )

    mock_requests_post.assert_called_with(
        'http://localhost:8000/application/messages',
        json=ANY
    )
