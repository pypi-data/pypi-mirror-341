from contextvars import ContextVar

session_id = ContextVar('session_id', default=None)
user_id = ContextVar('user_id', default=None)
app_id = ContextVar('app_id', default=None)
api_key = ContextVar('api_key', default=None)
last_assistant_message_id = ContextVar('last_assistant_message_id', default=None)
