# BranchCast — Devpost submission materials

**Draft status:** The repository, copy, session ID, and demo plan are ready. Real Twitch chat commands reached the queue and an approved branch appeared in an OBS Studio Browser Source on November 2, 2026. A Twitch broadcast test, video recording and upload, team confirmation, and Devpost submission are still pending. Review the copy against the actual finished demo before submitting; remove or revise any feature that was not shown or verified.

## Project title

BranchCast

## Short description

Turn Twitch chat ideas into visual branches. Viewers suggest an idea; the streamer reviews it and features selected branches on an OBS overlay.

## Project description — draft for Devpost

### Inspiration

Live streams are at their best when the audience can contribute to something the streamer is creating. We wanted to make those contributions visible and give the streamer a way to shape them before they appear on stream. BranchCast turns a starting idea into a canvas that a community can grow together.

### What it does

A streamer starts a BranchCast session and builds a visual canvas using labeled shapes. Viewers can fork the canvas in the local prototype. When the Twitch chat relay is configured, viewers can also suggest ideas using a chat command such as `!branch Moon garden | Flowers bloom above the clouds`.

Suggestions enter a review queue; they do not appear on stream automatically. The streamer approves or dismisses each branch. Approved ideas and their shapes appear on the BranchCast OBS browser-source display, which checks for updates automatically.

The sample sketch and enhancement in the application are **simulations using predefined shapes and styling**. They do not call an AI service. A separate OpenAI image-to-shapes experiment is included in the repository, but its live conversion has not been verified and it is not integrated into this demo.

### How we built it with Codex

We used OpenAI Codex throughout the build: developing the local Python and SQLite server; creating the streamer, viewer, queue and display interfaces; building the Twitch EventSub relay; adding approval controls and tests; and preparing setup and presentation materials. The project uses a lightweight browser interface and a separate local Twitch relay. Session data is stored on the local machine.

### Current scope

BranchCast is a local hackathon prototype. A broadcaster runs the server and Twitch relay on the machine that runs OBS. The project requires a Twitch developer application and an authorized user token for live chat. The server is not a public hosted collaboration service, and real AI conversion is not part of the demonstrated flow.

### What we want to improve next

We plan to verify and refine the live Twitch experience, expand the drawing editor and visual review tools, add secure hosted sessions for remote viewers, and evaluate real image-to-shape conversion when API access is available.

## Fields to copy into Devpost

- **Repository:** https://github.com/Battosai1806/branchcast
- **Codex session ID:** `01a190bf-8247-7f82-97b3-c27d42c4356e`
- **Platform:** Local application with a Twitch chat relay and OBS browser-source display.
- **Video URL:** Pending. Paste the final YouTube URL only after the real recording is uploaded and accessible.
- **Team:** Pending. The team must choose an authorized representative and confirm teammates have accepted required invitations.

## Live test and recording checklist

- [x] Twitch account authorized and token supplied to the local relay without sharing it in chat or committing it.
- [x] Run BranchCast and the relay using [TWITCH_SETUP.md](TWITCH_SETUP.md). A real `!branch` message reached the queue and was approved on November 2, 2026.
- [x] Verify an OBS Studio Browser Source shows an approved Twitch branch (user screenshot, November 2, 2026).
- [ ] Test the intended Twitch broadcast and capture footage showing the real chat-to-OBS interaction.
- [ ] Record real project footage on Twitch and the Codex build process using [DEMO.md](DEMO.md). Keep the video under three minutes. Hide credentials and use only material the team has permission to show.
- [ ] Upload the video to YouTube, check that judges can open it, and capture the URL. The event update says unlisted is acceptable; private is not.
- [ ] Verify setup from the public repository and confirm that no keys, tokens, `.env` files, or local database have been committed.
- [ ] Complete all Devpost fields, invite teammates as appropriate, and verify the entry says **Submitted**, not just Draft.

**Deadline:** November 2, 2026, 2:00 p.m. Pacific time / 4:00 p.m. Mexico City time. The event update advises that YouTube processing can take time and that the repository, video, and links should not be changed after the deadline until winners are announced.

Sources: [Official rules](https://twitchcon-codex.devpost.com/rules) and [final-weekend submission update](https://twitchcon-codex.devpost.com/updates/47341-final-weekend-make-your-project-come-alive).
