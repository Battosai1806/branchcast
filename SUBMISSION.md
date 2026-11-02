# Devpost submission draft — BranchCast

Review and edit every claim against the actual recorded demo. This file is a draft, not a submitted Devpost entry.

## Short description

BranchCast lets a Twitch community grow a streamer's idea together. Viewers suggest a new branch in chat, the streamer reviews it, and approved ideas appear in an OBS browser-source display.

## What it does

A streamer builds a starting idea canvas in a local BranchCast session. Viewers can create a separate fork in the local prototype or use `!branch title | description` in Twitch chat when the Twitch relay is configured. Chat suggestions enter a queue rather than appearing immediately on stream. The streamer approves or dismisses them, and approved branches appear on a browser-source overlay.

The sample-sketch feature is **simulated**: it uses predefined shapes and does not make an AI request. The separate OpenAI image-conversion experiment is not yet verified and must not be presented as a working live integration.

## How we used Codex

We used OpenAI Codex to turn the BranchCast idea into a local application, implement the canvas, server, persistence, viewer submissions and approval, build a Twitch EventSub relay, create an OBS display, write automated tests, and prepare setup and demo documentation. Include actual Codex development footage in the video.

## Links and submission fields

- Repository: https://github.com/Battosai1806/branchcast
- Main build Codex session ID: `01a190bf-8247-7f82-97b3-c27d42c4356e`
- Twitch and OBS setup: [TWITCH_SETUP.md](TWITCH_SETUP.md)
- Video: **not yet recorded or uploaded**. Add the actual judge-accessible YouTube link.
- Team and submitter: confirm and complete on Devpost. Team members must accept any required invitations.

## Before submission

- [ ] Verify the Twitch relay with a real channel and user-authorized token.
- [ ] Verify the actual OBS Browser Source and Twitch broadcast, and capture real footage without showing credentials.
- [ ] Record a video under three minutes showing the project working on Twitch and how Codex was used; upload it to YouTube with a visibility accessible to judges.
- [ ] Review setup instructions from a clean checkout and confirm no secrets are committed.
- [ ] Check eligibility, official rules, deadline, and all Devpost form fields. The event deadline is November 2, 2026, 2:00 p.m. Pacific time (4:00 p.m. Mexico City time).
- [ ] Enter the repository URL, video link, project description, Codex session ID, and team information. Confirm Devpost shows **Submitted**, not merely a saved draft.

Sources: [Official rules](https://twitchcon-codex.devpost.com/rules) and [final-weekend submission update](https://twitchcon-codex.devpost.com/updates/47341-final-weekend-make-your-project-come-alive).
