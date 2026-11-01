import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from pathlib import Path

import server


class ServerFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.old_db = server.DB_PATH
        server.DB_PATH = Path(cls.temp.name) / 'test.db'
        server.initialize()
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.httpd.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()
        server.DB_PATH = cls.old_db
        cls.temp.cleanup()

    def request(self, path, body=None, token=None):
        headers = {}
        if token:
            headers['X-Owner-Token'] = token
        data = None
        if body is not None:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body).encode()
        request = urllib.request.Request(self.base + path, data=data, headers=headers)
        with urllib.request.urlopen(request) as response:
            return json.load(response)

    def test_viewer_submission_approval_and_persistence(self):
        created = self.request('/api/sessions', {})
        path = '/api/sessions/' + created['id']
        owner_token = created['owner_token']
        public = self.request(path)
        self.assertFalse(public['is_owner'])
        self.assertNotIn('owner_token', public)
        self.assertNotIn('submissions', public)
        shapes = [{'type': 'rectangle', 'label': 'A viewer idea', 'x': 30, 'y': 40}]
        self.request(path + '/canvas', {'title': 'World', 'prompt': 'Explore', 'shapes': shapes}, owner_token)
        sub = self.request(path + '/submissions', {'author': 'viewer', 'title': 'A branch', 'description': 'An idea', 'shapes': shapes})
        self.assertEqual(self.request(path, token=owner_token)['submissions'][0]['id'], sub['id'])
        with self.assertRaises(urllib.error.HTTPError) as unauth:
            self.request(path + '/submissions/' + sub['id'] + '/approve', {})
        self.assertEqual(unauth.exception.code, 403)
        self.request(path + '/submissions/' + sub['id'] + '/approve', {}, owner_token)
        public = self.request(path)
        self.assertEqual(public['featured']['title'], 'A branch')
        self.assertEqual(public['featured']['shapes'], shapes)
        self.assertEqual(self.request(path, token=owner_token)['submissions'], [])
        server.initialize()
        self.assertEqual(self.request(path)['featured']['title'], 'A branch')

    def test_invalid_shapes_and_private_files_are_rejected(self):
        created = self.request('/api/sessions', {})
        path = '/api/sessions/' + created['id']
        with self.assertRaises(urllib.error.HTTPError) as invalid:
            self.request(path + '/submissions', {'author': 'viewer', 'title': 'idea', 'description': 'idea', 'shapes': [{'type': 'rectangle', 'label': 'x', 'x': -1, 'y': 2}]})
        self.assertEqual(invalid.exception.code, 400)
        for path in ('/.env.local', '/server.py', '/branchcast.db'):
            with self.assertRaises(urllib.error.HTTPError) as denied:
                self.request(path)
            self.assertEqual(denied.exception.code, 404)

    def test_competing_approvals_only_one_succeeds(self):
        created = self.request('/api/sessions', {})
        path = '/api/sessions/' + created['id']
        item = self.request(path + '/submissions', {'author': 'viewer', 'title': 'idea', 'description': 'a branch', 'shapes': []})

        def approve():
            try:
                self.request(path + '/submissions/' + item['id'] + '/approve', {}, created['owner_token'])
                return 200
            except urllib.error.HTTPError as error:
                return error.code

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: approve(), range(2)))
        self.assertEqual(sorted(results), [200, 404])
        self.assertEqual(self.request(path)['featured']['title'], 'idea')

    def test_owner_permissions_and_dismissal(self):
        created = self.request('/api/sessions', {})
        path = '/api/sessions/' + created['id']
        item = self.request(path + '/submissions', {'author': 'viewer', 'title': 'idea', 'description': 'a branch', 'shapes': []})
        with self.assertRaises(urllib.error.HTTPError) as denied:
            self.request(path + '/canvas', {'title': 'attack', 'prompt': '', 'shapes': []}, 'incorrect-token')
        self.assertEqual(denied.exception.code, 403)
        self.request(path + '/submissions/' + item['id'] + '/dismiss', {}, created['owner_token'])
        self.assertEqual(self.request(path, token=created['owner_token'])['submissions'], [])
        self.assertIsNone(self.request(path)['featured'])


if __name__ == '__main__':
    unittest.main()
