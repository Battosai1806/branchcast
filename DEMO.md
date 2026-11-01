# BranchCast: three-minute demo

This script demonstrates the **local prototype**. AI enhancement is simulated; Twitch chat, real AI conversion, and public internet sharing are not yet integrated. Say that explicitly in the presentation.

## Before recording

1. Run `python3 server.py` (`py server.py` on Windows) and open `http://127.0.0.1:8000` in the streamer browser. Keep the server and this browser open.
2. In Streamer editor, set the title to **The world of Aeris** and the prompt to **What stories live in the sky?** Add or rename a few shapes. Wait until the canvas says **Saved to this server**.
3. Choose **Copy viewer link** and open it in a second browser window or a private browser on the same computer. This ensures the viewer has a separate draft and no streamer token.
4. In the streamer window, open **OBS display**, choose **Copy OBS URL**, and add that URL to an OBS Browser Source. Set the source size to 1920 × 1080. Alternatively open the URL in a separate browser window as a display preview. Both must be on the computer running the server.
5. Rehearse a submission and approval, then refresh the queue and ensure there is no pending rehearsal item. Keep a screen recording of a successful rehearsal available as a fallback.

## Script

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:25 | Streamer editor | “BranchCast helps a streamer turn a starting idea into a collaborative creative session. Here is the world of Aeris and a few starting ideas.” |
| 0:25–0:55 | Move a shape and edit a label. Copy the viewer link. | “The streamer builds the starting canvas. A viewer can open a separate fork and build on it.” |
| 0:55–1:30 | Switch to viewer window, add a shape, enter a name, title, and description, then submit. | “A viewer adds their own branch and submits it for review. The original canvas stays separate from their fork.” |
| 1:30–2:00 | Return to the submission queue and approve the branch. | “The streamer controls which community submissions reach the stream.” |
| 2:00–2:25 | Show the OBS browser source updating. | “The approved branch appears automatically in this OBS display. This demo runs on a local server.” |
| 2:25–2:45 | Return to the canvas and select **Simulate enhancement**. | “This styling effect is a simulation. Real AI diagram conversion and Twitch events are the next integrations to verify.” |
| 2:45–3:00 | Show BranchCast title and repository. | “Our goal is to turn a live stream into a world the community can build together.” |

## If something goes wrong

- **Server offline:** restart `python3 server.py`, then reload the existing session URL. The session database survives a restart.
- **No streamer controls:** use the original streamer browser and the original session URL. The streamer token is stored in that browser, not in the viewer link.
- **OBS does not update:** verify the Browser Source URL contains the same session ID as the streamer window and ends with `#display`. Check that the local server is running; the display polls every two seconds.
- **Viewer link does not work on a phone or another computer:** the default server listens only on the same machine. Use a second browser window on the server computer for this demo.
- **Network or screen-sharing trouble:** play the rehearsal recording and identify it as a recording.

## Remaining delivery work

Real OpenAI conversion needs funded API access and a successful live test. Twitch needs an authorized app, a chat-reading token, and a real event test. Public multi-user hosting, authentication, and production permissions are also still needed before a public launch.
