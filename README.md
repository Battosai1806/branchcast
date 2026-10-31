# BranchCast

A collaborative live-stream brainstorming prototype for the Twitch hackathon. Stage 1 is a visual skeleton using simulated data; it does not require Twitch credentials or AI.

## Run locally

Open `index.html` in a modern browser, or serve the folder with `python3 -m http.server 8000` and visit http://localhost:8000.

## Explore the prototype

- **Streamer editor:** preview the shared canvas and edit its title.
- **Viewer editor:** write a simulated branch and submit it to the queue.
- **Submission queue:** approve an idea to feature it on the OBS preview, or dismiss it.
- **OBS display:** preview the currently featured idea.

State is held in the current browser tab and resets on refresh. Canvas tools, session sharing, live viewer counts, and OBS integration are visual placeholders. The prototype has no backend, persistence, Twitch connection, AI, or real drawing editor.

## Stage 2: feasibility experiments

These are separate local experiments, not yet integrated into the Stage 1 application. They use real external services and require your own credentials. Never commit tokens or share them in chat.

### AI diagram to editable shapes

Set an OpenAI API key in your shell, then run:

```sh
export OPENAI_API_KEY='your-key'
python3 feasibility/diagram.py path/to/rough-diagram.png
```

You can use `feasibility/sample-diagram.png` for a first smoke test. The script sends the image to the OpenAI Responses API and writes `diagram.json`. Open `feasibility/editor.html` in your browser, load that file, and edit the returned shapes. Drag their borders to move, resize using the bottom-right corner, edit labels directly, and download the result. The default model is `gpt-4o-mini`; override it with `OPENAI_MODEL` or `--model`. Output is an approximate reconstruction, not a pixel-perfect vectorization, and currently supports rectangles, ellipses, diamonds, and arrows. API usage can incur charges. See [OpenAI image inputs](https://developers.openai.com/api/docs/guides/images-vision) and [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

### Twitch chat event

Create a Twitch application and obtain a **user access token** for the same client with `user:read:chat`. Find the broadcaster and authorized user IDs. Install the dependency and run the listener:

```sh
python3 -m pip install -r requirements.txt
export TWITCH_CLIENT_ID='your-client-id'
export TWITCH_USER_TOKEN='your-user-access-token'
export TWITCH_BROADCASTER_ID='channel-user-id'
export TWITCH_USER_ID='authorized-user-id'
python3 feasibility/twitch_chat.py
```

After the subscription succeeds, send a chat message in that channel. The backend prints the chatter, message text, and EventSub message ID. Stop with Ctrl+C. The token is read from the process environment and never written to the repository. This is a local experiment: it does not refresh tokens, persist messages, or connect to the prototype UI. [Twitch authentication and EventSub setup](https://dev.twitch.tv/docs/chat/authenticating) and [EventSub WebSocket handling](https://dev.twitch.tv/docs/eventsub/handling-websocket-events) explain the requirements.

Run the offline checks with `python3 -m unittest discover -s tests`.

### Stage 2 completion checklist

1. Run the diagram converter on the sample and a real rough sketch. Load each output in the editor and confirm the shapes and layout are usable and can be edited and exported.
2. Run the Twitch listener, send a real message in the configured channel, and confirm the message appears in the listener output.
3. Record the results, including any recognition errors or connection issues. The offline tests use mocked services and do not establish live feasibility.

## Roadmap

1. Visual skeleton with simulated data (current stage).
2. Test AI diagram-to-editable-shapes and a real Twitch chat event reaching the backend (experiments implemented; live verification requires credentials).
3. Connect the editor, AI, sharing, viewer forks, submissions, persistence, approval, and automatically updated OBS display.
4. Polish the experience, test end to end, and prepare the hackathon demonstration.
