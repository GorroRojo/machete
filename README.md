# Machete: a live meeting copilot for Claude Code

Machete listens to the meeting you're in and, a few times an hour, offers to save you a step: a small card in the
corner of your screen. Tap ✓ and Claude does exactly that one thing; tap ✕ and it's gone. Nothing happens without
a tap.

Cards it can offer:

| Card | When | ✓ does |
|---|---|---|
| 🗂️ Prep (at the start) | There's a calendar event | Nothing (who's on the call, last notes, open items) |
| 📅 Date | "Let's meet Thursday at 3" | Adds it to your calendar, after a clash check |
| 🗓️ Find a time | "Let's find a time for all of us" | Drafts 2-3 free slots as options, or holds one on your calendar; never invites |
| 🌐 Time zones | "3 pm Eastern" | Nothing (your time and theirs) |
| ✅ Task | "I'll send Sam the numbers by Friday" | Creates it in your task tool, or a local reminder if you have none |
| ⚡ Heads-up | The meeting is discussing something with news that matters now (a reply minutes ago, a due invoice, today's news about the company) | Nothing (the fact, with a link to it) |
| 🔎 Answer | "What did we quote last time?", "How big is their team?" | Nothing (the answer while the question is open, with its source: your mail, docs, sheets, CRM, notes or, if on, the web) |
| 👤 Person | Someone in your notes or CRM comes up | Nothing (the one useful fact) |
| ✉️ Follow-up (at the end) | The meeting had other people | Drafts the follow-up email; never sends it |

At the end you also get a short report with an end-of-meeting checklist.

## How it works

1. A **listener** (`machete/listen.py`) runs in the background and notices when a meeting starts. It reads the live
   transcript from one source (set in `settings.md`):
   - **Wispr Flow**: its meeting recorder writes a live transcript file while recording; Machete reads it
     (tested on Windows).
   - **A transcript file**: any tool that writes the transcript to a text file *while* the meeting runs. Lines can
     be JSON, `Name: text` or plain text.
   - **Your mic and computer sound**, transcribed on this PC with faster-whisper. You start each meeting with
     `python machete/listen.py audio`.
2. When a meeting starts it opens the **cards window** (`machete/cards.py`), shows a consent reminder card, and
   starts a **Claude Code session** with `machete/session-prompt.md`. That session reads `settings.md`, checks your
   calendar, watches the transcript and offers cards.
3. It acts through **your own Claude connectors** (Google or Outlook calendar, Gmail or Outlook drafts, Slack drafts,
   ClickUp, Asana, Notion, Linear, a CRM, Google Sheets): whatever you have connected. With no task tool, a ✓ on a
   task sets a local reminder that pops up as a card on this computer.

## Requirements

- **Claude Code** with a Claude subscription (Pro or Max) or API access, recent enough to have the Monitor tool.
- **Python 3.11+** with tkinter (included in the python.org installers).
- **git**, or Claude Code downloads the zip instead.
- **A transcript source**: Wispr Flow, a tool that writes a live transcript file, or the audio option
  (`pip install -r requirements.txt` into the kit's `.venv`; a GPU helps but isn't required).
- Windows 10/11 is tested. macOS and Linux: the code is written to run there, but **untested**; the audio option
  can't capture computer sound on macOS without an extra loopback driver.

## Setup

Open Claude Code and paste this:

```
Set up Machete for me. Clone https://github.com/GorroRojo/machete into my home folder (if git isn't installed,
download https://github.com/GorroRojo/machete/archive/refs/heads/main.zip and unzip it there instead), then open
SETUP.md in that folder and follow it step by step.
```

It asks you five short questions (recorder, calendar, task tool, where your notes live, language), installs what's
needed, registers the background listener, runs a fake meeting to test it, and shows you a first card.

No git and no internet for Claude Code? `SETUP-PROMPT.md` is the same kit as one long prompt, with every file inside.

By hand: copy this folder anywhere, fill in `settings.md`, then

```
python -m venv .venv
.venv\Scripts\python machete\fake_meeting.py --check          # should print PASS
powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1
```

Try it without a call: `.venv\Scripts\python machete\fake_meeting.py --play wispr --dir data\fake-meetings` while a
listener runs with `--meetings-dir data\fake-meetings`.

**macOS (untested):** run the listener at login with a LaunchAgent: a plist in `~/Library/LaunchAgents/` whose
ProgramArguments are the kit's `.venv/bin/python` and `machete/listen.py`, with `RunAtLoad` and `KeepAlive` true and
`WorkingDirectory` set to the kit folder; load it with `launchctl load <plist>`.

## Privacy

- Machete's own files (transcript lines, cards, reports) stay in the kit's `data/` folder on your computer.
- The Claude session reads the transcript in order to help, so it goes to Claude like anything else in a Claude Code
  conversation. It is never sent to any other tool, person or website: the only thing that goes out is the single
  action you tapped ✓ (an event, a task, a draft), with only the words that action needs.
- Emails and chat messages are drafts only; it never sends them and never invites people.
- Your recorder has its own privacy terms (for example, Wispr Flow makes its own transcript). The audio option
  transcribes on your computer.
- **Tell people you're recording**: the first card of every meeting reminds you.
- **Private meetings switch it off** before a single line is read: events whose title or description has a word from
  "Meetings to skip" in `settings.md` (doctor, therapy, health, private... by default) or marked private. This needs a
  calendar connector; without one, set `Copilot: off` in settings before a private call.
- The cards window is hidden from screen shares on Windows 10 version 2004 or newer (see `settings.md` to show it).

## Limits (true today)

- Rare on purpose: about 6 cards an hour at most, none in the first 2 minutes except answers to questions asked out loud. Less-sure items go on the end list.
- The transcript is a few seconds behind and mishears names; Machete checks names against your notes, the invite or
  the CRM before using them.
- Not supported live: **Granola, Otter, Fireflies** and other cloud notetakers don't write a live transcript file on
  your computer that Machete can read, so they aren't supported. **Zoom / Google Meet captions** only work if some
  tool saves them to a file as the meeting goes.
- Each card's action depends on your connectors. Machete can't do what your connectors can't.
- The first time the session uses a connector, Claude Code may ask permission in its terminal window; allow the ones
  you want it to use.
- Local reminders only appear while the computer is on and the listener runs.
- One meeting at a time.

## Files

| File | What |
|---|---|
| `settings.md` | Your settings, in plain English |
| `machete/listen.py` | The background listener and transcript sources |
| `machete/cards.py` | The cards window and the command that adds cards |
| `machete/session-prompt.md` | What the Claude session does |
| `machete/follow.py` | Follows `data/live.log` for the session |
| `machete/remind.py` | Local reminders (no task tool) |
| `machete/fake_meeting.py` | Fake meeting: `--check` test, `--play` demo |
| `machete/start_session.ps1` / `.sh` | Starts the Claude session (Windows / macOS-Linux, the latter untested) |
| `machete/install_listener.ps1` | Registers the listener at sign-in (Windows) |
| `machete/common.py` | Shared paths and settings reader |
