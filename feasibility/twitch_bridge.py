"""Relay Twitch !branch chat commands to a local BranchCast submission queue."""
import argparse
import asyncio
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import quote, urlparse

from twitch_chat import listen


def parse_branch(event):
    """Return a bounded submission for !branch title | description, or None."""
    message = event.get('message')
    if not isinstance(message, dict):
        return None
    text = message.get('text')
    if not isinstance(text, str) or not text.lower().startswith('!branch '):
        return None
    title, separator, description = text[8:].partition('|')
    title, description = title.strip(), description.strip()
    author = event.get('chatter_user_name') or event.get('chatter_user_login') or 'Twitch viewer'
    if not isinstance(author, str) or not separator or not title or not description:
        return None
    return {'author': author.strip()[:40] or 'Twitch viewer', 'title': title[:80], 'description': description[:240]}


def relay(event, base, session_id):
    submission = parse_branch(event)
    if submission is None:
        return False
    path = f'{base}/api/sessions/{quote(session_id, safe="")}'
    with urllib.request.urlopen(path, timeout=5) as response:
        canvas = json.load(response)
    shapes = canvas.get('shapes', [])
    # Keep every command on a copy; viewer ideas never mutate the streamer canvas.
    shapes = shapes[:99] + [{'type': 'rectangle', 'label': submission['title'], 'x': 50, 'y': 50}]
    submission['shapes'] = shapes
    request = urllib.request.Request(path + '/submissions', data=json.dumps(submission).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=5) as response:
        json.load(response)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', required=True, help='BranchCast session ID, from the session URL')
    parser.add_argument('--server', default='http://127.0.0.1:8000', help='Local BranchCast server URL')
    args = parser.parse_args()
    url = urlparse(args.server)
    if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost', '::1') or url.path not in ('', '/') or url.query or url.fragment or url.username or url.password:
        parser.error('Use a local HTTP server URL, such as http://127.0.0.1:8000.')
    if not args.session or len(args.session) > 80 or not all(c.isalnum() or c in '-_' for c in args.session):
        parser.error('Invalid BranchCast session ID.')
    keys = ['TWITCH_CLIENT_ID', 'TWITCH_USER_TOKEN', 'TWITCH_BROADCASTER_ID', 'TWITCH_USER_ID']
    missing = [name for name in keys if not os.getenv(name)]
    if missing:
        parser.error('Missing environment variables: ' + ', '.join(missing))
    base = args.server.rstrip('/')
    try:
        with urllib.request.urlopen(f'{base}/api/sessions/{quote(args.session, safe="")}', timeout=5) as response:
            json.load(response)
    except (urllib.error.URLError, ValueError) as error:
        sys.exit(f'Cannot find the local BranchCast session: {error}')
    def on_event(event):
        try:
            if relay(event, base, args.session):
                print('Twitch branch received; awaiting streamer approval.', flush=True)
        except (OSError, ValueError, KeyError) as error:
            print(f'Could not add Twitch branch: {error}', file=sys.stderr, flush=True)
    print('Listening for !branch title | description. Streamer approval is required.', flush=True)
    try:
        asyncio.run(listen(*(os.environ[name] for name in keys), on_event=on_event))
    except KeyboardInterrupt:
        print('\nStopped.')
    except (urllib.error.URLError, RuntimeError) as error:
        sys.exit(f'Twitch connection failed: {error}')


if __name__ == '__main__':
    main()
