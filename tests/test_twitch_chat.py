import asyncio
import importlib
import json
import sys
import types
import unittest
import urllib.error
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

# The transport is replaced with an in-process EventSub fixture. The real
# dependency is only needed when connecting to Twitch.
fake_websockets = types.ModuleType('websockets')
fake_websockets.exceptions = types.ModuleType('websockets.exceptions')
fake_websockets.exceptions.WebSocketException = type('WebSocketException', (Exception,), {})
fake_websockets.connect = lambda *args, **kwargs: None
with patch.dict(sys.modules, {'websockets': fake_websockets, 'websockets.exceptions': fake_websockets.exceptions}):
    twitch = importlib.import_module('feasibility.twitch_chat')


class Socket:
    def __init__(self, messages):
        self.messages = iter(messages)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return json.dumps(next(self.messages))
        except StopIteration:
            raise StopAsyncIteration


class TwitchTests(unittest.IsolatedAsyncioTestCase):
    async def test_welcome_subscribes_and_chat_is_delivered_once(self):
        event = {'metadata': {'message_type': 'notification', 'message_id': 'event-1'}, 'payload': {'event': {'chatter_user_name': 'viewer', 'message': {'text': 'Hello world'}}}}
        messages = [
            {'metadata': {'message_type': 'session_welcome'}, 'payload': {'session': {'id': 'session-1'}}},
            event, event,
            {'metadata': {'message_type': 'revocation'}, 'payload': {}},
        ]
        output = StringIO()
        with patch.object(twitch.websockets, 'connect', return_value=Socket(messages)), patch.object(twitch, 'subscribe') as subscribe, redirect_stdout(output):
            with self.assertRaisesRegex(RuntimeError, 'revoked'):
                await twitch.listen('client', 'token', 'broadcaster', 'user')
        subscribe.assert_called_once_with('session-1', 'client', 'token', 'broadcaster', 'user')
        self.assertEqual(output.getvalue().count('Hello world'), 1)
        self.assertIn('viewer', output.getvalue())

    async def test_callback_receives_twitch_event_once(self):
        event = {'chatter_user_name': 'viewer', 'message': {'text': '!branch Moon | A garden'}}
        notification = {'metadata': {'message_type': 'notification', 'message_id': 'event-1'}, 'payload': {'event': event}}
        messages = [
            {'metadata': {'message_type': 'session_welcome'}, 'payload': {'session': {'id': 'session-1'}}},
            notification, notification,
            {'metadata': {'message_type': 'revocation'}, 'payload': {}},
        ]
        delivered = []
        with patch.object(twitch.websockets, 'connect', return_value=Socket(messages)), patch.object(twitch, 'subscribe'):
            with self.assertRaisesRegex(RuntimeError, 'revoked'):
                await twitch.listen('client', 'token', 'broadcaster', 'user', on_event=delivered.append)
        self.assertEqual(delivered, [event])
    async def test_rejected_subscription_fails_without_reconnecting(self):
        welcome = {'metadata': {'message_type': 'session_welcome'}, 'payload': {'session': {'id': 'session-1'}}}
        error = urllib.error.HTTPError('https://api.twitch.tv/', 401, 'Unauthorized', {}, None)
        with patch.object(twitch.websockets, 'connect', return_value=Socket([welcome])) as connect, patch.object(twitch, 'subscribe', side_effect=error):
            with self.assertRaisesRegex(RuntimeError, 'HTTP 401'):
                await twitch.listen('client', 'token', 'broadcaster', 'user')
        self.assertEqual(connect.call_count, 1)
    def test_subscription_uses_websocket_session_and_user_ids(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *_): return False
            def read(self): return b'{"data": []}'
        with patch('urllib.request.urlopen', return_value=Response()) as request:
            twitch.subscribe('session', 'client', 'token', 'broadcaster', 'user')
            payload = json.loads(request.call_args.args[0].data)
        self.assertEqual(payload['type'], 'channel.chat.message')
        self.assertEqual(payload['condition'], {'broadcaster_user_id': 'broadcaster', 'user_id': 'user'})
        self.assertEqual(payload['transport'], {'method': 'websocket', 'session_id': 'session'})


if __name__ == '__main__':
    unittest.main()
