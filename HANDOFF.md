# BranchCast — implementation and test handoff

**Status as of November 1, 2026:** BranchCast is a local hackathon prototype, not a completed or production-ready application. The repository contains a working local collaboration flow, two separate feasibility experiments, and a demonstration script. The work was fast because it uses a small Python standard-library server, plain HTML/CSS/JavaScript, SQLite, and simple prototype UI—not a full cloud product.

The [README](README.md) explains how to run the project and [DEMO.md](DEMO.md) contains a three-minute presentation. This document is the detailed follow-up list. A checked item below means it was implemented or verified at the time of this handoff; a pending item needs someone to complete and verify it.

## 1. What exists today

| Area | What actually works | What it does not yet do |
| --- | --- | --- |
| Streamer canvas | Add, rename, move, and delete labeled shapes; save the canvas title and prompt. | Freehand drawing, arrows/connectors, resizing, undo/redo, zoom, and real AI enhancement are not implemented in the main app. |
| Viewer fork | Copy a session's canvas into a browser-local draft, edit it, and submit it. | A draft is not continuously synchronized to other devices, and a `127.0.0.1` link cannot be opened from a different machine. |
| Submission queue | An owner can see pending submissions, approve one, or dismiss one. | The queue shows labels rather than a full visual branch preview; moderation, spam prevention, and real Twitch identity are absent. |
| OBS display | A separate browser page polls the local server and shows the last approved idea. | A live OBS Studio capture was not verified; remote hosting, production reliability, and full shape-layout rendering are not implemented. |
| Persistence | A local SQLite database stores session, canvas, and submitted/featured data. Drafts and owner tokens are held in browser local storage. | There is no shared cloud database, account recovery, backups, migration system, or production multi-user protection. Clearing browser storage loses the owner token. |
| AI feasibility | A separate Python script sends an image to OpenAI and requests structured shape data; a separate HTML editor can load that data. | The live request has not succeeded; the main app does not call this script, and its **Simulate enhancement** button is only a style change. |
| Twitch feasibility | A separate Python EventSub listener can subscribe to chat messages when correctly configured; offline tests simulate Twitch events. | No real Twitch event has been received, and the listener is not connected to the main app. |
| Demo | A local three-minute script and presentation view exist. | The project has not been verified against the full competition submission requirements, and no final recording/submission has been produced. |

The owner token and session links are prototype mechanisms, not a complete permission system. Do not expose the local Python server to the public internet as it stands.

## 2. Repository and local setup

Repository: <https://github.com/Battosai1806/branchcast>. The repository is public, so never commit API keys, Twitch tokens, secrets, database files, private chat messages, or `.env.local`. The existing `.gitignore` excludes local env files, `diagram.json`, and `branchcast.db`; double-check `git status` and staged files before each push.

1. Clone the repository and use Python 3.10 or newer.
2. From the project folder, run `python3 server.py` (on Windows, `py server.py` may be appropriate).
3. Open `http://127.0.0.1:8000` on the **same computer**. Keep the server running.
4. The first page creates a session. The owner token is saved in that browser's local storage; save the resulting URL and keep that browser profile. Opening the root URL without the existing session ID creates another session.
5. Copy the viewer link from the streamer page and open it in another browser profile or private window on the same computer. Copy the OBS URL into another browser window for the local test.
6. Stop the server with Ctrl+C. Restarting it with the same database preserves sessions; clearing local storage loses the owner token even if the database survives.

`server.py` defaults to `127.0.0.1:8000`, and `BRANCHCAST_DB` can point to a different SQLite file for disposable tests. The application does **not** automatically read `.env.local`; the standalone AI script reads `OPENAI_API_KEY` from its process environment.

## 3. Immediate blockers and decisions

### 3.1 OpenAI API billing / credits

**Observed result:** The OpenAI API key was created for the **Personal / Default project** and stored only in `.env.local` on the original machine. The selected key lifetime was 30 days from creation; verify whether it has expired before using it. The file is not in Git and will not appear on a partner's clone. A live request for the sample diagram reached OpenAI but returned HTTP 429 with `insufficient_quota` / `credit_balance_exhausted`. A promotional-credit eligibility check returned `not_qualified` for the connected account at that time. No successful live conversion has been recorded.

**What “billing” means:** This is payment for API usage by the project; it is not a customer checkout, subscription system for BranchCast users, or a need to hire a payment manager. The account owner must decide whether to fund the API or use another provider. A ChatGPT subscription is separate from API billing; some eligible plans may offer API credits, subject to eligibility and activation. OpenAI's current [API credit guidance](https://developers.openai.com/api/docs/guides/chatgpt-api-credits) explains the offer and limits. Check the account's [billing page](https://platform.openai.com/settings/organization/billing) and [limits page](https://platform.openai.com/settings/organization/limits) before running paid requests. No credit card or account secret should be sent in chat, committed, or added to the app's client-side code.

**Partner follow-up:**

1. Decide who owns and funds the OpenAI API project, or decide on a different AI provider. The original user's named project was not visible in the connector; the configured key uses Default project. Resolve account/project ownership before relying on that key for shared work.
2. If using OpenAI, configure a budget, alerts, and a hard limit if desired and available; check model access and expiry. Avoid assuming alerts alone stop charges.
3. Each developer should use an authorized secret setup for their own environment. Do not copy the original machine's `.env.local` into Git. Export `OPENAI_API_KEY` into the shell that starts the test. The script does not load `.env.local` itself.
4. Run `python3 feasibility/diagram.py feasibility/sample-diagram.png`. The expected result is `diagram.json` and a nonzero count of sensible shapes. Then test at least one representative hand-drawn diagram with labels and arrows.
5. Open `feasibility/editor.html`, load the output, edit and export it, and compare layout and labels with the source. Record the model, image type, success/failure, rough cost, and observed recognition mistakes without recording the API key or sensitive image content.

**Done when:** At least one real supported image converts successfully, the result can be edited and exported, errors are understandable, and a budget owner has agreed to the ongoing cost. This confirms feasibility, not integration into the main application.

### 3.2 Twitch app, credentials, and real chat event

**Observed result:** The listener exists in `feasibility/twitch_chat.py`; offline tests emulate a welcome, subscription, duplicate message, and revocation. The required Twitch environment variables were not configured, and no real Twitch event has been received. The last checked Linux environment also lacked `pip` and the `websockets` package; install them in a supported Python environment or virtual environment.

**Partner follow-up:**

1. Register a Twitch app in the [Twitch Developer Console](https://dev.twitch.tv/console/apps); enable required account security and configure the app's redirect URI as described in [Twitch app registration](https://dev.twitch.tv/docs/authentication/register-app).
2. For this local WebSocket experiment, obtain a **user access token** with `user:read:chat` for the same Twitch application and identify the authorized user's numeric ID and broadcaster's numeric ID. For a self-test, the broadcaster and authorized user can be the same account. Follow [Twitch chat authentication and EventSub](https://dev.twitch.tv/docs/chat/authenticating); hosted bot requirements can differ from this local flow.
3. Install the project dependency with `python3 -m pip install -r requirements.txt`. Set `TWITCH_CLIENT_ID`, `TWITCH_USER_TOKEN`, `TWITCH_BROADCASTER_ID`, and `TWITCH_USER_ID` in the listener's process environment. Never commit the token, include it in client code, or paste it into a public issue.
4. Run `python3 feasibility/twitch_chat.py`. Confirm it reports a successful subscription, then send a chat message in the target channel. Verify the listener prints that message and its ID. Do not publish raw user chat logs without considering privacy.
5. Test expired/revoked tokens, a wrong client ID, missing scope, a disconnected socket, a Twitch-requested reconnect, and duplicate messages. Twitch notes that events may be redelivered and that events lost during an unexpected disconnect are not replayed; see [EventSub WebSocket handling](https://dev.twitch.tv/docs/eventsub/handling-websocket-events/).

**Done when:** A real message from the intended Twitch channel reaches the backend, the result is documented, and reconnection/authorization failures have clear behavior. This test does not by itself connect Twitch to the BranchCast UI.

## 4. Pending implementation work

### 4.1 Connect real AI to the main editor

- [ ] Decide the supported input: upload a sketch, draw freehand in the app, or both. The current main canvas supports simple nodes, not freehand ink.
- [ ] Add a server-side AI endpoint. Keep the API key on the backend, validate file type and size, provide timeouts and helpful quota/rate-limit errors, and avoid automatically sending user content without an explicit action.
- [ ] Define one shared diagram format and an import/mapping layer. The separate AI experiment returns `rectangle`, `ellipse`, `diamond`, and `arrow` with `x`, `y`, `width`, and `height`. The main server currently accepts only `rectangle`, `ellipse`, and `diamond` with `x`, `y`, and `label`. The coordinates, dimensions, and arrow representation must be reconciled; there is currently no automatic import.
- [ ] Show a preview and let the user accept, edit, retry, or discard AI output. Treat unrecognized/empty/refused output as a visible error, not as a successful conversion.
- [ ] Agree on and enforce cost controls, input retention, and privacy expectations. Make any simulated fallback visibly labeled.
- [ ] Test malformed input, unsupported image, size limits, long request, bad key, exhausted balance, rate limit, model refusal, invalid schema, and poor-quality recognition.

### 4.2 Connect Twitch to BranchCast

- [ ] Decide the purpose of chat events: joining a session, suggesting content, triggering a command, or another defined interaction. The current listener only prints chat text.
- [ ] Implement an appropriate Twitch authorization flow and safely manage tokens, expiration, validation, revocation, and refresh. Do not expose tokens in the browser or logs.
- [ ] Bridge authorized events into the correct BranchCast session; define identity mapping and how a streamer grants or revokes access. Do not rely on display names as secure identities.
- [ ] Handle duplicate delivery, reconnects, missed events, rate limits, and listener restarts. Define behavior when Twitch is offline.
- [ ] Add moderation controls, input validation, and limits before viewer-generated content can appear on stream.
- [ ] Verify using a real channel and record the result. Test unauthorized users and revoked permissions as well as the happy path.

### 4.3 Remote sessions and real persistence

- [ ] Choose a hosting environment and deployment approach. The present development server binds to localhost by default. Do not treat `--host 0.0.0.0` as production deployment or as sufficient security.
- [ ] Provide a reachable HTTPS URL and a durable database with migrations, backups, restore testing, and an explicit data-retention plan. Ensure separate sessions and users are isolated.
- [ ] Replace the browser-local owner token with an authenticated owner identity and recovery mechanism. Current access is lost if that browser's local storage is cleared. Establish roles and permissions for streamer, viewers, moderators, and OBS display.
- [ ] Add abuse protection for session creation, submissions, and AI calls: validation, quotas, rate limits, privacy controls, and appropriate moderation.
- [ ] Address simultaneous edits, stale saves, retry and conflict handling, multiple browser tabs, reconnects, and large audiences. The current client autosaves whole-canvas snapshots and can overwrite concurrent work; it is not a collaborative editing engine.
- [ ] Test sharing between genuinely separate devices and networks, server restarts, expired/revoked links, unauthorized access, and database restoration.

### 4.4 Editor and review experience

- [ ] Decide the intended drawing model and add missing freehand drawing, connectors/arrows, resize, select/multi-select, undo/redo, and zoom/pan as needed for the hackathon scope.
- [ ] Replace label-only review and OBS shape chips with a visual rendering of the submitted layout if that is required for the final presentation.
- [ ] Verify keyboard access, focus behavior, screen-reader labels, error states, small screens, and reduced-motion preferences. Movement by keyboard exists, but comprehensive accessibility testing has not been completed.
- [ ] Test invalid and long text, 100-shape limit, empty drafts, duplicate submissions, local-storage loss, retry after save failure, and session switching.

### 4.5 OBS and delivery

- [ ] Test the generated URL in **actual OBS Studio**, not just a headless browser. Confirm source dimensions, transparency/background requirements, font loading, refresh, reconnect, and readability on stream.
- [ ] Exercise the intended hosted URL in OBS, including restarts, expired sessions, and bad network conditions. The current display polls every two seconds.
- [ ] Verify the hackathon's current eligibility, Twitch integration, submission format, deadline, demo length, and any required assets from the event's official rules. These requirements have not been verified here.
- [ ] Rehearse the [demo script](DEMO.md), record a successful run, prepare fallback footage, and submit only after the team agrees the live integrations and claims are accurate.

## 5. Test inventory and evidence

### Already run successfully

- `python3 -m unittest discover -s tests -v`: **9 offline tests** passed. These cover mocked OpenAI response handling, input validation, mocked Twitch subscription and event deduplication, local HTTP permission checks, submission/approval, persistence within the test database, rejection of private-file routes, and competing approvals.
- A headless Edge/Playwright test, `tests/browser_flow.cjs`, passed with separate browser contexts: streamer edits a shape, viewer forks and submits, streamer approves, and an already-open display updates. This was a local browser test, not a test in OBS Studio or across remote machines.
- Python compilation and JavaScript syntax checks passed at the time of the last application change.

### Still required before claiming a working end-to-end product

- [ ] Successful real AI image-to-shape conversion, representative sketch quality evaluation, and editing the output.
- [ ] Real Twitch chat message received for the intended broadcaster, plus reconnect and authorization failure cases.
- [ ] Full browser flow against the **hosted** app using at least two different devices/networks and independent users.
- [ ] Real OBS Browser Source test against the intended deployment and across connection interruptions.
- [ ] Full permissions tests: unauthenticated viewers, wrong owner, moderator, revoked tokens, session isolation, and attempts to access private content.
- [ ] Recovery tests: server restart, database backup/restore, lost owner credentials, network drop, stale canvas save, and repeated/duplicate requests.
- [ ] Security and abuse review before public exposure: authentication, secret handling, HTTPS, input size and rate limits, output escaping, logs, and content moderation.
- [ ] Accessibility and responsive tests across supported browsers and devices; test keyboard and screen reader paths.
- [ ] Load test with a realistic number of viewers and submissions and document acceptable latency and failure behavior.
- [ ] Final end-to-end rehearsal with the actual demo hardware, stream setup, and contingency recording.

## 6. Suggested order of work

1. Decide the hackathon's required scope, deadline, funding, and whether a local-only demonstration is acceptable.
2. Resolve API access and perform the AI feasibility test; independently complete the Twitch live event test.
3. Choose hosting and identity/permission design. Build remote sessions and protect the service before exposing it.
4. Integrate the real AI and Twitch flows into the main app, then verify the OBS source against the hosted environment.
5. Run the remaining tests, rehearse and record the demo, and submit only what has been verified.
