# Cholk: Twitch and OBS setup

The Twitch relay reads chat commands and adds them to the streamer's submission queue. The streamer approves each idea before it appears on the OBS display.

## Set up Twitch

1. Sign in to Twitch, verify your email, and enable two-factor authentication. Register an application in the [Twitch Developer Console](https://dev.twitch.tv/console/apps), using a unique name and OAuth redirect URL `http://localhost:3000`. See [Twitch app registration](https://dev.twitch.tv/docs/authentication/register-app).
2. Install Python 3.10+, pip, the [Twitch CLI](https://dev.twitch.tv/docs/cli/), and OBS Studio. Install the relay dependency from the repository:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

   On Windows, use `py -m pip install -r requirements.txt`.
3. Start Cholk with `python3 server.py` (Windows: `py server.py`) and open `http://127.0.0.1:8000`. Keep the streamer browser open and copy the `session` value from its URL.
4. Configure the Twitch CLI with your application's client ID and secret. Authorize a **user access token** with `user:read:chat` for the broadcaster account. See the [Twitch CLI token instructions](https://dev.twitch.tv/docs/cli/token-command/). Find the authorized user's numeric Twitch ID through [Get Users](https://dev.twitch.tv/docs/api/get-started/). When the broadcaster and authorized user are the same account, use that ID for both variables below.
5. In a second terminal, set these environment variables using your own values:

   ```bash
   export TWITCH_CLIENT_ID='your-client-id'
   export TWITCH_USER_TOKEN='your-user-access-token'
   export TWITCH_BROADCASTER_ID='broadcaster-numeric-id'
   export TWITCH_USER_ID='authorized-user-numeric-id'
   ```

   In Windows PowerShell, use `$env:TWITCH_CLIENT_ID = 'your-client-id'` and the same format for the other three variables. Run the relay with the session ID from step 3:

   ```bash
   python3 feasibility/twitch_bridge.py --session YOUR_SESSION_ID
   ```

   On Windows, use `py feasibility/twitch_bridge.py --session YOUR_SESSION_ID`. Wait for the subscription confirmation.
6. In your Twitch channel's chat, send:

   ```text
   !branch Moon garden | Flowers bloom above the clouds
   ```

   The suggestion appears in **Submission queue**. Approve it to feature it on the display.

## Set up OBS

In Cholk, open **OBS display**, copy the URL, and add it as an OBS **Browser Source** on the computer running Cholk. A 1920×1080 source is recommended.

A real Twitch chat suggestion was received, approved, and shown through OBS on a Twitch broadcast on November 2, 2026.

Keep the server and relay running during the demo. Do not share tokens or client secrets, or expose the local development server to the public internet. The relay does not refresh expired tokens.
