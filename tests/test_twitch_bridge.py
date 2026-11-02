import asyncio
import importlib.util
import json
import tempfile
import threading
import types
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
import sys

import server
from test_twitch_chat import Socket, twitch

fake_chat = types.ModuleType('twitch_chat')
fake_chat.listen = None
with patch.dict(sys.modules, {'twitch_chat': fake_chat}):
    spec = importlib.util.spec_from_file_location('twitch_bridge', Path(__file__).resolve().parents[1] / 'feasibility' / 'twitch_bridge.py')
    bridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bridge)


class TwitchBridgeTests(unittest.TestCase):
    def test_parse_rejects_invalid_and_bounded_content(self):
        self.assertIsNone(bridge.parse_branch({'message': {'text': '!branch no separator'}}))
        self.assertIsNone(bridge.parse_branch({'message': {'text': '!branch title | '}}))
        self.assertIsNone(bridge.parse_branch({'message': {'text': 'ordinary chat'}}))
        result = bridge.parse_branch({'message': {'text': '!BRANCH ' + 'x' * 90 + ' | ' + 'y' * 250}, 'chatter_user_name': 'viewer'})
        self.assertEqual(len(result['title']), 80)
        self.assertEqual(len(result['description']), 240)
        self.assertEqual(result['author'], 'viewer')

    def test_chat_command_is_queued_but_not_auto_featured(self):
        with tempfile.TemporaryDirectory() as temp:
            old = server.DB_PATH
            server.DB_PATH = Path(temp) / 'test.db'
            server.initialize()
            httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                import urllib.request
                base = f'http://127.0.0.1:{httpd.server_port}'
                request = urllib.request.Request(base + '/api/sessions', data=b'{}', headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(request) as response:
                    created = json.load(response)
                event = {'chatter_user_name': 'TwitchViewer', 'message': {'text': '!branch Moon garden | Flowers on the moon'}}
                notification = {'metadata': {'message_type': 'notification', 'message_id': 'chat-1'}, 'payload': {'event': event}}
                messages = [
                    {'metadata': {'message_type': 'session_welcome'}, 'payload': {'session': {'id': 'session-1'}}},
                    notification, notification,
                    {'metadata': {'message_type': 'revocation'}, 'payload': {}},
                ]
                def receive(payload):
                    bridge.relay(payload, base, created['id'])
                with patch.object(twitch.websockets, 'connect', return_value=Socket(messages)), patch.object(twitch, 'subscribe'):
                    with self.assertRaisesRegex(RuntimeError, 'revoked'):
                        asyncio.run(twitch.listen('client', 'token', 'broadcaster', 'user', on_event=receive))
                url = base + '/api/sessions/' + created['id']
                with urllib.request.urlopen(url) as response:
                    public = json.load(response)
                self.assertIsNone(public['featured'])
                request = urllib.request.Request(url, headers={'X-Owner-Token': created['owner_token']})
                with urllib.request.urlopen(request) as response:
                    owned = json.load(response)
                self.assertEqual(len(owned['submissions']), 1)
                self.assertEqual(owned['submissions'][0]['author'], 'TwitchViewer')
                self.assertEqual(owned['submissions'][0]['title'], 'Moon garden')
                self.assertEqual(owned['submissions'][0]['shapes'][-1]['label'], 'Moon garden')
                decision = urllib.request.Request(url + '/submissions/' + owned['submissions'][0]['id'] + '/approve', data=b'{}', headers={'Content-Type': 'application/json', 'X-Owner-Token': created['owner_token']})
                with urllib.request.urlopen(decision) as response:
                    self.assertEqual(response.status, 200)
                with urllib.request.urlopen(url) as response:
                    self.assertEqual(json.load(response)['featured']['title'], 'Moon garden')
            finally:
                httpd.shutdown()
                httpd.server_close()
                thread.join()
                server.DB_PATH = old


if __name__ == '__main__':
    unittest.main()
