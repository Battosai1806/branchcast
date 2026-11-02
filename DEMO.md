# BranchCast: three-minute Twitch demo

The hackathon requires footage of the project working on Twitch and footage showing how it was built with Codex. Twitch chat and the OBS Browser Source have been demonstrated locally; record after verifying the actual Twitch broadcast using [TWITCH_SETUP.md](TWITCH_SETUP.md). Do not show tokens, account secrets, or unapproved viewer content. The sample sketch and enhancement are simulations: identify them as such.

## Preparation

1. Start BranchCast and its Twitch relay, authorize the broadcaster account, and confirm the relay reports a successful subscription.
2. Open the streamer session and add its OBS display URL as a Browser Source. Confirm it is visible in a test Twitch broadcast and that the same session ID is used throughout.
3. Send a `!branch title | description` message in the actual Twitch channel, approve it, and verify the OBS source updates. Prepare an additional original chat suggestion for the recording.
4. Open the Codex conversation and show the actual development work without displaying any credentials. Prepare a recording fallback and check audio/scene framing.

## Suggested script

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:20 | Twitch stream and BranchCast | “BranchCast turns a streamer's starting idea into a community collaboration.” |
| 0:20–0:45 | Streamer canvas | “The streamer creates the starting canvas and chooses what goes on stream.” |
| 0:45–1:20 | Actual Twitch chat | “A viewer submits an idea using `!branch`, and it arrives in the streamer's queue.” Send a real chat command. |
| 1:20–1:50 | Submission queue | Approve the actual Twitch suggestion and explain that approval keeps the streamer in control. |
| 1:50–2:15 | OBS source visible on Twitch | Show the approved branch appearing on the running broadcast. |
| 2:15–2:35 | Sample-sketch simulation | “This example uses predefined shapes; live AI conversion is not yet integrated.” |
| 2:35–2:55 | Codex conversation and repository | Show how Codex helped build the project and summarize the idea. |

Keep the finished video under three minutes, upload it to YouTube with a judge-accessible visibility, and provide its link in Devpost. See [SUBMISSION.md](SUBMISSION.md) and the [official rules](https://twitchcon-codex.devpost.com/rules).

## Fallbacks

- If Twitch is disconnected, check the relay terminal and reauthorize if needed. Do not claim simulated chat is a live Twitch connection.
- If the display does not update, confirm OBS and the streamer page reference the same session and the local server is running.
- If live AI is not funded, use the explicitly labeled simulation. If a recording must be used as a backup, identify it as a recording.

## Recording notes and copy-ready narration

Record a real run; this is a script, not evidence that the live integration has passed. Keep the final edit below three minutes and remove setup terminals containing account credentials.

**0:00–0:20 — Twitch stream and BranchCast.** “Live streams are more fun when the audience can contribute to what the streamer is making. BranchCast lets a community grow an idea together, while the streamer stays in control of what appears on stream.”

**0:20–0:45 — Streamer canvas.** “The streamer starts with a simple visual canvas. Here we are building a world together. I can add and move ideas, then invite the community to suggest a new branch.” Show the local app and a canvas edit.

**0:45–1:20 — Real Twitch chat.** “A viewer sends a branch in Twitch chat using a short command. BranchCast receives that suggestion and places it in the streamer's review queue.” Show a real chat message and the resulting queue item. If this has not been verified, stop and fix the connection before recording this section.

**1:20–1:50 — Review.** “The streamer can review the suggestion and decide whether to feature or dismiss it. Nothing is published to the overlay until it is approved.” Show the approval action.

**1:50–2:15 — OBS on Twitch.** “Once approved, the branch appears in our OBS display so it can become part of the live stream.” Show the actual OBS source and the Twitch broadcast updating. Confirm the broadcast is permitted and visible for the recording.

**2:15–2:35 — Simulation.** “The sketch example uses predefined shapes for this demo. Real AI image conversion is a separate experiment that we have not verified yet.” Show the labeled simulation briefly.

**2:35–2:55 — Codex.** “We used OpenAI Codex to build the local app, the Twitch relay, the viewer and streamer flows, the OBS display, and tests. BranchCast is our starting point for turning a chat into a shared creative canvas.” Show actual Codex development context and the repository.

Before uploading, check the audio, edit length, visibility, and that the link works in a signed-out browser. The organizer's [submission update](https://twitchcon-codex.devpost.com/updates/47341-final-weekend-make-your-project-come-alive) says unlisted YouTube videos are acceptable; private videos are not. Keep an unedited backup in case the team needs to fix the final cut.
