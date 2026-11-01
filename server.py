"""Local BranchCast prototype server. Run `python3 server.py` to start."""
import argparse
import hmac
import json
import os
import secrets
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv('BRANCHCAST_DB', ROOT / 'branchcast.db'))
STATIC = {'/': ('index.html', 'text/html; charset=utf-8'), '/index.html': ('index.html', 'text/html; charset=utf-8'), '/style.css': ('style.css', 'text/css; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8')}
MAX_BODY = 128 * 1024


def database():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def initialize():
    with database() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, owner_token TEXT NOT NULL, title TEXT NOT NULL, prompt TEXT NOT NULL, shapes TEXT NOT NULL, featured TEXT, updated_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id), author TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL, shapes TEXT NOT NULL, created_at INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'pending');
        ''')


def validate_shapes(value):
    if not isinstance(value, list) or len(value) > 100:
        raise ValueError('Shapes must be a list with at most 100 items.')
    result = []
    for shape in value:
        if not isinstance(shape, dict) or shape.get('type') not in ('rectangle', 'ellipse', 'diamond'):
            raise ValueError('Invalid shape type.')
        label = shape.get('label')
        if not isinstance(label, str) or len(label) > 100:
            raise ValueError('Shape labels must be 100 characters or fewer.')
        position = {}
        for key in ('x', 'y'):
            n = shape.get(key)
            if isinstance(n, bool) or not isinstance(n, (int, float)) or not 0 <= n <= 100:
                raise ValueError('Shape coordinates must be percentages between 0 and 100.')
            position[key] = n
        result.append({'type': shape['type'], 'label': label, **position})
    return result


def text_field(data, name, limit, required=True):
    value = data.get(name)
    if not isinstance(value, str) or len(value.strip()) > limit or (required and not value.strip()):
        raise ValueError(f'{name} must be {"nonempty and " if required else ""}at most {limit} characters.')
    return value.strip()


def public_session(row):
    return {'id': row['id'], 'title': row['title'], 'prompt': row['prompt'], 'shapes': json.loads(row['shapes']), 'featured': json.loads(row['featured']) if row['featured'] else None, 'updated_at': row['updated_at']}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Request paths contain session IDs; keep logs free of bearer-like links.
        pass

    def respond(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        size = int(self.headers.get('Content-Length', '0'))
        if size < 1 or size > MAX_BODY:
            raise ValueError('Invalid request size.')
        data = json.loads(self.rfile.read(size))
        if not isinstance(data, dict):
            raise ValueError('Expected a JSON object.')
        return data

    def owner(self, row):
        token = self.headers.get('X-Owner-Token', '')
        return bool(token) and hmac.compare_digest(token, row['owner_token'])

    def do_GET(self):
        path = urlparse(self.path).path
        if path in STATIC:
            filename, mime = STATIC[path]
            body = (ROOT / filename).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        parts = path.strip('/').split('/')
        if len(parts) != 3 or parts[:2] != ['api', 'sessions']:
            return self.respond(404, {'error': 'Not found.'})
        with database() as db:
            row = db.execute('SELECT * FROM sessions WHERE id = ?', (parts[2],)).fetchone()
            if not row:
                return self.respond(404, {'error': 'Session not found.'})
            result = public_session(row)
            result['is_owner'] = self.owner(row)
            if result['is_owner']:
                rows = db.execute("SELECT * FROM submissions WHERE session_id = ? AND status = 'pending' ORDER BY created_at DESC", (row['id'],)).fetchall()
                result['submissions'] = [{'id': s['id'], 'author': s['author'], 'title': s['title'], 'description': s['description'], 'shapes': json.loads(s['shapes']), 'created_at': s['created_at']} for s in rows]
            return self.respond(200, result)

    def do_POST(self):
        try:
            self.post()
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as error:
            self.respond(400, {'error': str(error)})

    def post(self):
        parts = urlparse(self.path).path.strip('/').split('/')
        data = self.read_json()
        if parts == ['api', 'sessions']:
            session_id, token = secrets.token_urlsafe(18), secrets.token_urlsafe(32)
            shapes = [{'type': 'rectangle', 'label': 'The world of Aeris', 'x': 14, 'y': 43}, {'type': 'ellipse', 'label': 'The floating gardens', 'x': 58, 'y': 20}, {'type': 'diamond', 'label': 'The sky sailors', 'x': 58, 'y': 65}]
            with database() as db:
                db.execute('INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)', (session_id, token, 'The world of Aeris', 'What stories, places, and people live in this world?', json.dumps(shapes), None, time.time_ns()))
                db.commit()
            return self.respond(201, {'id': session_id, 'owner_token': token})
        if len(parts) < 4 or parts[:2] != ['api', 'sessions']:
            return self.respond(404, {'error': 'Not found.'})
        session_id, operation = parts[2], parts[3:]
        with database() as db:
            row = db.execute('SELECT * FROM sessions WHERE id = ?', (session_id,)).fetchone()
            if not row:
                return self.respond(404, {'error': 'Session not found.'})
            if operation == ['submissions']:
                author = text_field(data, 'author', 40)
                title = text_field(data, 'title', 80)
                description = text_field(data, 'description', 240)
                shapes = validate_shapes(data.get('shapes'))
                submission_id = secrets.token_urlsafe(16)
                db.execute('INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (submission_id, session_id, author, title, description, json.dumps(shapes), time.time_ns(), 'pending'))
                db.commit()
                return self.respond(201, {'id': submission_id})
            if not self.owner(row):
                return self.respond(403, {'error': 'Streamer access required.'})
            if operation == ['canvas']:
                title = text_field(data, 'title', 80)
                prompt = text_field(data, 'prompt', 300, required=False)
                shapes = validate_shapes(data.get('shapes'))
                db.execute('UPDATE sessions SET title = ?, prompt = ?, shapes = ?, updated_at = ? WHERE id = ?', (title, prompt, json.dumps(shapes), time.time_ns(), session_id))
                db.commit()
                return self.respond(200, {'ok': True})
            if len(operation) == 3 and operation[0] == 'submissions' and operation[2] in ('approve', 'dismiss'):
                item = db.execute("SELECT * FROM submissions WHERE id = ? AND session_id = ? AND status = 'pending'", (operation[1], session_id)).fetchone()
                if not item:
                    return self.respond(404, {'error': 'Pending submission not found.'})
                status = 'approved' if operation[2] == 'approve' else 'dismissed'
                db.execute('UPDATE submissions SET status = ? WHERE id = ?', (status, item['id']))
                if status == 'approved':
                    featured = {'title': item['title'], 'author': item['author'], 'description': item['description'], 'shapes': json.loads(item['shapes'])}
                    db.execute('UPDATE sessions SET featured = ?, updated_at = ? WHERE id = ?', (json.dumps(featured), time.time_ns(), session_id))
                db.commit()
                return self.respond(200, {'ok': True})
            return self.respond(404, {'error': 'Not found.'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    initialize()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'BranchCast running at http://{args.host}:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping BranchCast.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
