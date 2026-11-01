# BranchCast

A collaborative live-stream brainstorming prototype for the Twitch hackathon. Stage 3 is underway: the local app now saves sessions and connects viewer forks, submissions, approval, and an updating OBS display. AI enhancement is simulated and the Twitch listener remains a separate feasibility experiment.

## Run locally

Run `python3 server.py` from the repository, then visit http://127.0.0.1:8000 in a modern browser. On Windows, `py server.py` works when Python is installed. Keep the server running while using the app; a static server or opening `index.html` directly cannot provide session functionality.

## Explore the prototype

- **Streamer editor:** add, move, rename, or remove shapes; edit the title and prompt; copy a viewer link.
- **Viewer editor:** fork the canvas, change your copy, and submit it to the queue.
- **Submission queue:** review shape labels, approve an idea to feature it on the OBS display, or dismiss it.
- **OBS display:** copy the display URL into an OBS Browser Source. It refreshes automatically when an idea is approved.

Sessions and submissions persist in the local SQLite file `branchcast.db` (ignored by Git); viewer drafts and the streamer access token are stored in the browser. Keep the original streamer browser and session URL: clearing its local storage loses streamer access. The OBS browser source can use the same server on the same computer. The viewer link uses the server's address, so `127.0.0.1` links work only on that computer. This is a local development prototype, not public hosting: it does not provide accounts, production security, remote collaboration over the internet, or reliable multi-user synchronization. The simulated enhancement changes shape styles; it does not call AI. Twitch is not connected to the app.

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

1. Visual skeleton with simulated data (implemented).
2. Test AI diagram-to-editable-shapes and a real Twitch chat event reaching the backend (experiments implemented; live verification requires credentials).
3. Connect the editor, AI, sharing, viewer forks, submissions, persistence, approval, and automatically updated OBS display (local prototype started; hosted collaboration, real AI, and Twitch integration remain).
4. Polish the experience, test end to end, and prepare the hackathon demonstration.
