# BranchCast: Twitch and OBS setup

The local Twitch relay reads chat commands and places them in the streamer's approval queue. AI enhancement is simulated and does not require a paid API.

1. Sign in to Twitch, verify your email, and enable two-factor authentication. Register an application in the [Twitch Developer Console](https://dev.twitch.tv/console/apps), using a unique name and OAuth redirect URL `http://localhost:3000`. Follow [Twitch app registration](https://dev.twitch.tv/docs/authentication/register-app).
2. Install Python 3.10+, pip, [Twitch CLI](https://dev.twitch.tv/docs/cli/), and OBS Studio. In the repository, create a virtual environment and install the dependency:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Start the local application with `.\.venv\Scripts\python.exe server.py` and open `http://127.0.0.1:8000`. Keep the streamer browser open. Copy the `session` value from the browser URL.
4. Using the [Twitch CLI token instructions](https://dev.twitch.tv/docs/cli/token-command/), configure the CLI with the application details and authorize a user token with `user:read:chat` for the broadcaster account. Find the authorized user's Twitch ID through [Get Users](https://dev.twitch.tv/docs/api/get-started/). When the broadcaster and authorized user are the same account, use that same ID for both environment variables. Never expose the token or Client Secret on stream or commit them to Git.
5. In a second terminal, configure the environment variables described in [README.md](README.md): `TWITCH_CLIENT_ID`, `TWITCH_USER_TOKEN`, `TWITCH_BROADCASTER_ID`, and `TWITCH_USER_ID`. Run `.\.venv\Scripts\python.exe feasibility/twitch_bridge.py --session SESSION_ID`, replacing `SESSION_ID` with the value copied in step 3. Wait for a successful subscription message.
6. In the actual Twitch channel chat, type `!branch Moon garden | Flowers bloom above the clouds`. The suggestion should appear in the streamer's **Submission queue**. Approve it to feature it on the overlay.
7. In the app, open **OBS display**, copy the display URL, and add it as an OBS Browser Source on the same computer running BranchCast. Use a 1920×1080 source and check that the approved branch updates. Then test it during an actual Twitch broadcast. Do not show credentials in the recording.

The Twitch integration must be tested with a real channel before claiming it works live. The relay does not start a stream or send chat messages. Its current process holds credentials in environment memory and does not refresh expired tokens. Session sharing and the server remain local; do not expose the development server to the public internet.

For submission, follow the [official rules](https://twitchcon-codex.devpost.com/rules), record a video under three minutes showing BranchCast working on Twitch and how Codex was used, and upload it to YouTube so judges can access it.
