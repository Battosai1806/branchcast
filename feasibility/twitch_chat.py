"""Receive a real Twitch chat event via EventSub WebSocket."""
import asyncio
import json
import os
import sys
import urllib.error
import urllib.request

try:
    import websockets
except ImportError:
    sys.exit("Install dependencies first: python -m pip install -r requirements.txt")

URL = "wss://eventsub.wss.twitch.tv/ws"

def subscribe(session_id, client_id, token, broadcaster_id, user_id):
    body = {"type": "channel.chat.message", "version": "1", "condition": {"broadcaster_user_id": broadcaster_id, "user_id": user_id}, "transport": {"method": "websocket", "session_id": session_id}}
    req = urllib.request.Request("https://api.twitch.tv/helix/eventsub/subscriptions", data=json.dumps(body).encode(), headers={"Client-Id": client_id, "Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=8) as response:
        return json.load(response)

async def listen(client_id, token, broadcaster_id, user_id):
    url = URL
    transferred = False
    seen = set()
    while True:
        try:
            async with websockets.connect(url, ping_interval=None) as socket:
                print("Connected to Twitch EventSub.", flush=True)
                async for raw in socket:
                    message = json.loads(raw)
                    kind = message.get("metadata", {}).get("message_type")
                    payload = message.get("payload", {})
                    if kind == "session_welcome":
                        if not transferred:
                            await asyncio.to_thread(subscribe, payload["session"]["id"], client_id, token, broadcaster_id, user_id)
                            print("Subscribed to channel.chat.message; waiting for chat...", flush=True)
                        transferred = False
                    elif kind == "notification":
                        message_id = message["metadata"]["message_id"]
                        if message_id in seen:
                            continue
                        seen.add(message_id)
                        if len(seen) > 1000:
                            seen.clear()
                            seen.add(message_id)
                        event = payload.get("event", {})
                        print(json.dumps({"chatter": event.get("chatter_user_name"), "text": event.get("message", {}).get("text"), "message_id": message_id}, ensure_ascii=False), flush=True)
                    elif kind == "session_reconnect":
                        url = payload["session"]["reconnect_url"]
                        transferred = True
                        break
                    elif kind == "revocation":
                        raise RuntimeError("Twitch revoked the subscription; check authorization.")
                else:
                    url, transferred = URL, False
                    await asyncio.sleep(2)
        except (OSError, websockets.exceptions.WebSocketException) as exc:
            print(f"Connection lost ({exc}); reconnecting...", file=sys.stderr, flush=True)
            url, transferred = URL, False
            await asyncio.sleep(3)

def main():
    keys = ["TWITCH_CLIENT_ID", "TWITCH_USER_TOKEN", "TWITCH_BROADCASTER_ID", "TWITCH_USER_ID"]
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        sys.exit("Missing environment variables: " + ", ".join(missing))
    try:
        asyncio.run(listen(*(os.environ[key] for key in keys)))
    except KeyboardInterrupt:
        print("\nStopped.")
    except (urllib.error.URLError, RuntimeError) as exc:
        sys.exit(f"Twitch subscription failed: {exc}")

if __name__ == "__main__":
    main()
