# Set up Machete, a live meeting copilot (paste all of this into Claude Code)

You are setting up **Machete** on this computer for me. Machete listens to my meetings and offers rare one-tap cards
(dates, find-a-time, tasks, facts, people, time zones, a prep card at the start, a follow-up draft at the end);
nothing acts without my ✓. Everything you need is in this message; download nothing from the internet except the
Python packages named in step 4, and only if I choose the audio option.

1. **Ask me these five questions in one short message** (offer the choices; one line each):
   1. Recorder: **Wispr Flow** / **a tool that writes a live transcript file** (which file or folder?) /
      **my mic and computer sound, transcribed on this PC**.
   2. Calendar: which one do I use? Check which Claude connectors you have (calendar, email, Slack, tasks, CRM,
      sheets) and tell me what you found.
   3. Task tool (ClickUp, Asana, Notion, Linear, other, or none = local reminders on this computer).
   4. Where my notes live (a folder on this computer, Notion, Drive, a CRM, or nowhere).
   5. Card language (or "the meeting's language").
2. Create the folder `machete` in my home folder (unless I name another) and write **every file below exactly as
   given**, at the path in its heading. Then fill in `settings.md` from my answers (Transcript source: `wispr`,
   `file` with the Transcript file path, or `audio`; my tools; where to look things up; language). If a calendar
   connector shows my name and time zone, fill those in too. Change nothing else.
3. Check Python 3.11+ with tkinter (`python -c "import tkinter"`). If it's missing, tell me how to install it and stop.
   Create a venv inside the folder: `python -m venv .venv`.
4. Only for the audio option: `.venv` python `-m pip install -r requirements.txt`.
5. Run the fake-meeting test with the venv python: `machete/fake_meeting.py --check`. It must print PASS; if not,
   fix the cause and run it again.
6. Register the background listener (ask me first; it starts at sign-in and runs hidden):
   - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1`.
   - macOS (untested, say so): a LaunchAgent plist in `~/Library/LaunchAgents/` running the venv's python with
     `machete/listen.py`, WorkingDirectory the kit folder, RunAtLoad and KeepAlive true; `launchctl load` it.
   - Audio option: also tell me that each meeting starts with `python machete/listen.py audio`.
7. Show me a first card: `machete/cards.py add date "Thu · 15:00\nQ3 review with Sam\nTest card: tap ✓" --source
   "Machete setup"`, then open the window in the background (`machete/cards.py window`, with pythonw on Windows).
   Ask me to tap ✓, confirm the tap appeared in `data/live.log`, then `machete/cards.py done <id> "Setup works"`.
8. Finish with five lines: which card actions will work with my connectors, how to pause (`Copilot: off` in
   settings.md), how to uninstall (`install_listener.ps1 -Remove` and delete the folder), that private meetings are
   skipped by the keywords in settings.md, and to tell people when I'm recording.


## File: `settings.md`

`````markdown
# Machete settings

Plain English. Change anything, save, and it applies from the next meeting. The listener reads only the lines under
"Listener"; everything else is read by the Claude session at the start of each meeting.

## Listener
- Transcript source: wispr
  (wispr = Wispr Flow's live meeting transcript · file = a transcript file another tool writes while the meeting runs ·
  audio = your mic and computer sound, transcribed on this PC; start each meeting with `python machete/listen.py audio`)
- Transcript file: (only for source = file: the file, or the folder where the tool writes one file per meeting)
- Meeting ends after minutes of silence: 20
- Whisper model: small
  (only for source = audio: tiny, base, small, medium or large-v3-turbo; bigger is better and slower)
- Language: auto
- Copilot: on
  (off = the listener ignores every meeting until you set it back to on)

## About you
- Your name: (write it here; names on the calendar invite are checked against it)
- Who you work for: (optional: company, team or "freelance")
- Your time zone: (e.g. America/New_York; empty = this computer's)

## Your tools (Claude uses whatever connectors you have; leave a line empty if you don't use it)
- Calendar: (e.g. Google Calendar or Outlook, through your Claude connector)
- Tasks: (e.g. ClickUp, Asana, Notion, Linear, Todoist; empty = local reminders on this computer)
- Email drafts: (e.g. Gmail or Outlook; drafts only, never sent)
- Chat drafts: (e.g. Slack; drafts only, never sent)
- CRM: (e.g. HubSpot; empty if none)
- Spreadsheets: (e.g. a Google Sheet with sales or sign-ups; give its name or link)

## Where to look things up
- Notes folder: (a folder on this computer with your notes, e.g. an Obsidian vault; people's notes help the person card)
- Other places: (e.g. a Notion workspace, a Drive folder, the CRM, the calendar invite's description)
- Web lookups: on (public facts only: a company, product, price, law or term; never quotes or private details
  from the meeting. Write "off" to never search the web.)

## Meetings to skip (the copilot switches itself off before reading a single line)
- Any event whose title or description has: doctor, dentist, therapy, therapist, psychologist, psychiatrist, health,
  medical, clinic, appointment, private, personal, 1:1 HR, interview (add or remove words)
- Any event you mark private in your calendar (private visibility), and any meeting with no calendar event if you
  write "yes" here: no

## Card rules (edit freely)
- Nothing in the first 2 minutes, except answers to questions asked out loud.
- At most one card every 2 minutes, about 6 an hour; never the same thing twice. A question asked out loud may
  get its answer card any time.
- Only with a clear trigger plus a confirming sign; anything less sure goes on the end-of-meeting list.
- Headline 2 to 5 words; at most two short lines under it; the source small at the bottom.
- Cards in the meeting's language (or always in: ________).
- Card kinds on: answer, heads-up, date, find a time, task, person, time zones, prep at start, follow-up email at end
  (delete any you don't want).
- Work hours for "find a time" offers: 9:00 to 18:00 on weekdays.

## Screen sharing
- The cards window is hidden from screen shares by default (Windows 10 version 2004 or newer).
- To show it on a share (for a demo), create an empty file named `show-on-share` in the `data` folder, then restart
  the window; delete the file afterwards.
`````

## File: `README.md`

`````markdown
<p align="left"><img src="assets/machete-logo-animated.svg" width="88" alt="Machete logo: a hand with the index finger raised and a cheat sheet slipping out of the cuff"></p>

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
- **Using Fathom?** Keep it: Fathom writes up the call afterwards, Machete works during it. Fathom doesn't keep a live
  transcript on your computer, so run Machete with the `audio` source (your mic and computer sound, transcribed
  locally) next to it. The `audio` source is **beta and untested in a real meeting so far**; real meetings have run
  on Wispr Flow.
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
`````

## File: `requirements.txt`

`````text
# Wispr Flow and file sources need nothing beyond Python 3.11+ with tkinter.
# Only the audio source (mic + computer sound transcribed on this PC) needs these:
faster-whisper>=1.0
soundcard>=0.4
numpy
`````

## File: `.gitignore`

`````text
data/
.venv/
__pycache__/
`````

## File: `.claude/settings.json`

`````json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(python machete/cards.py:*)",
      "Bash(python machete/remind.py:*)",
      "Bash(python -u machete/follow.py:*)",
      "PowerShell(python machete/cards.py:*)",
      "PowerShell(python machete/remind.py:*)",
      "PowerShell(python -u machete/follow.py:*)",
      "Write(data/**)",
      "Edit(data/**)"
    ]
  }
}
`````

## File: `machete/common.py`

`````python
"""Shared paths and helpers for Machete. Everything Machete writes stays in the kit's data folder on this PC."""
from __future__ import annotations

import datetime as dt
import os
import pathlib
import re

KIT = pathlib.Path(__file__).resolve().parent.parent
# MACHETE_DATA lets the fake-meeting test use its own folder.
DATA = pathlib.Path(os.environ.get("MACHETE_DATA") or (KIT / "data"))
LOG = DATA / "live.log"            # what the Claude session watches
SETTINGS = KIT / "settings.md"

# Lines in settings.md like "- Transcript source: wispr" (the listener reads only these keys).
KEYS = {
    "transcript source": "source",          # wispr | file | audio
    "transcript file": "file",              # a file, or a folder (newest file in it), for source = file
    "meeting ends after minutes of silence": "end_minutes",
    "whisper model": "model",               # for source = audio
    "language": "language",
    "copilot": "copilot",                   # on | off
}
DEFAULTS = {"source": "wispr", "file": "", "end_minutes": "20", "model": "small", "language": "auto", "copilot": "on"}


def settings() -> dict:
    out = dict(DEFAULTS)
    try:
        text = SETTINGS.read_text(encoding="utf-8")
    except FileNotFoundError:
        return out
    for line in text.splitlines():
        m = re.match(r"^\s*[-*]\s*\**([A-Za-z ]+?)\**\s*:\s*\**\s*(.*?)\s*$", line)
        if m and m.group(1).strip().lower() in KEYS:
            value = m.group(2).strip().strip("`").strip()
            if value and not value.startswith("("):
                out[KEYS[m.group(1).strip().lower()]] = value
    return out


def live_line(text: str, at: dt.datetime | None = None) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    stamp = (at or dt.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{stamp} [machete] {' '.join(text.split())}\n")


def status(text: str) -> None:
    """The listener's own log: when things start and stop, never meeting text."""
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / "listener.log").open("a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')} {text}\n")
`````

## File: `machete/listen.py`

`````python
"""Machete listener: turns the meeting you are in into a live transcript for the Machete Claude Code session.

It watches one transcript source, chosen in settings.md ("Transcript source"):
  wispr  Wispr Flow's own live transcript. While Wispr records a meeting it writes
         <meetings folder>/<id>/live.ndjson (one JSON line per phrase; speaker.source "mic" = you, "system" = the call).
         The meeting has ended when Wispr writes the finished upload.ogg, or after N minutes of silence.
         Meetings folder: %APPDATA%\\Wispr Flow\\meetings on Windows (tested). Elsewhere pass --meetings-dir.
  file   Any tool that writes the transcript to a text file WHILE the meeting runs. "Transcript file" is that file,
         or a folder (then the newest file in it that is being written is the meeting). Lines may be JSON
         ({"text": "...", "speaker": "..."}), "Name: text", or plain text. Ends after N minutes with no new lines.
  audio  Your microphone and your computer's sound, transcribed on this PC with faster-whisper. No meeting signal
         exists here, so you start it yourself:  python machete/listen.py audio   (Ctrl+C or N silent minutes ends it).

Output, all inside the kit's data folder (never sent anywhere):
  data/<meeting id>/segments.jsonl   {"who", "wall", "text"}
  data/live.log                      one line per phrase, what the session watches:
      2026-03-12T14:03:12 [machete] @others: let's meet Thursday at 3 pm Eastern
  plus "[machete] start <id>", "[machete] end <id> (...)" and the cards window's "[machete] tap ..." lines.

When a meeting starts it opens the cards window, adds the consent reminder card and starts the Machete Claude Code
session (start_session.ps1 / start_session.sh). If <data>/<meeting id>/off exists (the session writes it for private
meetings) nothing more is read. It also shows due reminders (remind.py) as cards.

Usage:
    python machete/listen.py                     # background listener for the wispr / file sources (runs until stopped)
    python machete/listen.py audio               # one meeting from mic + system audio
    python machete/listen.py --no-session --once --meetings-dir <dir>   # tests (see test_fake_meeting.py)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import platform
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import DATA, KIT, live_line, settings, status  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ACTIVE_AGE = 20  # a transcript written in the last N seconds = a meeting now
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
IS_WIN = platform.system() == "Windows"


def default_wispr_dir() -> pathlib.Path:
    if IS_WIN:
        return pathlib.Path(os.environ.get("APPDATA", "")) / "Wispr Flow" / "meetings"
    # Untested guess for macOS; pass --meetings-dir if Wispr keeps meetings somewhere else.
    return pathlib.Path.home() / "Library" / "Application Support" / "Wispr Flow" / "meetings"


# ---------------------------------------------------------------- meetings (one class per source)

class Meeting:
    """Shared state: where its output goes, what was read already, whether it was switched off."""
    def __init__(self, meeting_id: str):
        self.id = meeting_id
        self.out = DATA / meeting_id
        self.out.mkdir(parents=True, exist_ok=True)
        self.state_path = self.out / "state.json"
        st = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {}
        self.offset = st.get("offset", 0)
        self.seen = set(st.get("seen", []))
        self.lines = st.get("lines", 0)
        self.started = st.get("started")
        self.last_new = time.time()

    def save(self) -> None:
        self.state_path.write_text(json.dumps({"offset": self.offset, "seen": sorted(self.seen)[-2000:],
                                               "lines": self.lines, "started": self.started}), encoding="utf-8")

    def off(self) -> bool:
        return (self.out / "off").exists()

    def write(self, new: list[dict]) -> int:
        if new:
            stamps = [s.pop("_at", None) for s in new]
            with (self.out / "segments.jsonl").open("a", encoding="utf-8") as fo:
                for s in new:
                    fo.write(json.dumps(s, ensure_ascii=False) + "\n")
            for s, at in zip(new, stamps):
                live_line(f"@{s['who']}: {s['text']}", at)
            self.lines += len(new)
            self.last_new = time.time()
        self.save()
        return len(new)

    def read_new(self, path: pathlib.Path) -> list[bytes]:
        """Whole new lines appended to `path` since the last read."""
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return []
        if size < self.offset:  # rewritten: read again from the top
            self.offset = 0
        if size == self.offset:
            return []
        with path.open("rb") as fh:
            fh.seek(self.offset)
            chunk = fh.read(size - self.offset)
        cut = chunk.rfind(b"\n")
        if cut < 0:
            return []  # half a line so far
        self.offset += cut + 1
        return chunk[: cut + 1].splitlines()


class WisprMeeting(Meeting):
    def __init__(self, folder: pathlib.Path, end_minutes: float):
        super().__init__(folder.name)
        self.folder, self.end_minutes = folder, end_minutes

    def ended(self) -> bool:
        if (self.folder / "upload.ogg").exists() or (self.folder / "refined.ndjson").exists():
            return True  # Wispr writes these when recording stops (a short pause is not the end)
        try:
            age = time.time() - (self.folder / "live.ndjson").stat().st_mtime
        except FileNotFoundError:
            return True
        return age > self.end_minutes * 60

    def step(self) -> int:
        new = []
        for raw in self.read_new(self.folder / "live.ndjson"):
            try:
                e = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            text = " ".join(str(e.get("text") or "").split())
            if not text or "id" not in e or e["id"] in self.seen:
                continue
            self.seen.add(e["id"])
            who = "me" if (e.get("speaker") or {}).get("source") == "mic" else "others"
            at = dt.datetime.fromtimestamp(e["startEpochMs"] / 1000) if e.get("startEpochMs") else dt.datetime.now()
            new.append({"who": who, "wall": at.strftime("%H:%M:%S"), "text": text, "_at": at})
        return self.write(new)


def active_wispr(root: pathlib.Path) -> pathlib.Path | None:
    """The newest Wispr meeting folder whose live.ndjson is being written and isn't finished."""
    best = None
    try:
        folders = [p for p in root.iterdir() if p.is_dir()]
    except FileNotFoundError:
        return None
    for d in folders:
        try:
            mt = (d / "live.ndjson").stat().st_mtime
        except FileNotFoundError:
            continue
        finished = (d / "refined.ndjson").exists() or (d / "upload.ogg").exists()
        if time.time() - mt < ACTIVE_AGE and not finished and (best is None or mt > best[0]):
            best = (mt, d)
    return best[1] if best else None


class FileMeeting(Meeting):
    def __init__(self, path: pathlib.Path, end_minutes: float):
        stamp = dt.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y%m%d-%H%M")
        super().__init__(f"{''.join(ch if ch.isalnum() or ch in '-_' else '-' for ch in path.stem)[:40]}-{stamp}")
        self.path, self.end_minutes = path, end_minutes
        if not self.started:
            self.offset = 0  # read what was already written, then follow

    def ended(self) -> bool:
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return True
        return age > self.end_minutes * 60

    def step(self) -> int:
        new = []
        for raw in self.read_new(self.path):
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            who, text = "others", line
            if line.startswith("{"):
                try:
                    e = json.loads(line)
                    text = str(e.get("text") or "")
                    sp = str(e.get("speaker") or e.get("who") or e.get("source") or "others")
                    who = "me" if sp.lower() in ("me", "mic", "you", "self") else sp
                except ValueError:
                    pass
            elif ": " in line[:40]:
                sp, text = line.split(": ", 1)
                who = "me" if sp.strip().lower() in ("me", "you") else sp.strip()
            text = " ".join(text.split())
            if text:
                new.append({"who": "_".join(who.split()) or "others", "wall": dt.datetime.now().strftime("%H:%M:%S"),
                            "text": text})
        return self.write(new)


def active_file(target: str, done: dict) -> pathlib.Path | None:
    """The transcript file being written now (a file, or the newest file in a folder)."""
    if not target:
        return None
    p = pathlib.Path(os.path.expandvars(os.path.expanduser(target)))
    try:
        files = [p] if p.is_file() else [f for f in p.iterdir() if f.is_file()] if p.is_dir() else []
        best = max(files, key=lambda f: f.stat().st_mtime, default=None)
        if best is None:
            return None
        st = best.stat()
    except OSError:
        return None
    if time.time() - st.st_mtime < ACTIVE_AGE and done.get(str(best)) != st.st_size:
        return best
    return None


# ---------------------------------------------------------------- start of a meeting

def python_for(windowless: bool) -> str:
    exe = pathlib.Path(sys.executable)
    if windowless and IS_WIN and (exe.parent / "pythonw.exe").exists():
        return str(exe.parent / "pythonw.exe")
    return str(exe)


def cards(*args: str) -> None:
    subprocess.run([python_for(False), str(HERE / "cards.py"), *args], cwd=KIT, creationflags=NO_WINDOW,
                   capture_output=True)


def open_window(enabled: bool = True) -> None:
    if not enabled:
        return
    subprocess.Popen([python_for(True), str(HERE / "cards.py"), "window"], cwd=KIT,
                     creationflags=NO_WINDOW | getattr(subprocess, "DETACHED_PROCESS", 0),
                     start_new_session=not IS_WIN)


def on_start(m: Meeting, session: bool, window: bool) -> None:
    live_line(f"start {m.id}")
    cards("clear", "--keep-meeting", m.id)  # leftovers of earlier meetings
    cards("add", "consent", "Tell people you're recording\n\"I'm transcribing this to take notes\"",
          "--meeting", m.id)
    open_window(window)
    if session:
        if IS_WIN:
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(HERE / "start_session.ps1"),
                   "-Meeting", m.id]
        else:
            cmd = ["sh", str(HERE / "start_session.sh"), m.id]
        subprocess.run(cmd, cwd=KIT, creationflags=NO_WINDOW)
    status(f"meeting {m.id} started; session {'asked' if session else 'off'}")


def check_reminders(window: bool) -> None:
    try:
        import remind
        if remind.fire_due():
            open_window(window)
    except Exception as e:  # never stop listening over a reminder
        status(f"reminders failed: {type(e).__name__}")


# ---------------------------------------------------------------- main loops

def run_listener(args, cfg) -> None:
    lock = DATA / "listener.lock"
    try:
        if lock.exists() and time.time() - lock.stat().st_mtime < 30:
            print("another listener is running"); return
    except OSError:
        pass
    end_minutes = float(args.end_minutes or cfg["end_minutes"])
    source = cfg["source"].lower()
    root = pathlib.Path(args.meetings_dir) if args.meetings_dir else default_wispr_dir()
    status(f"listening, source {source}")
    done_files: dict = {}
    meeting = None
    while True:
        lock.write_text(str(os.getpid()))
        check_reminders(not args.no_window)
        if meeting is None and cfg.get("copilot", "on").lower() != "off":
            if source == "wispr":
                f = active_wispr(root)
                meeting = WisprMeeting(f, end_minutes) if f else None
            elif source == "file":
                f = active_file(args.file or cfg["file"], done_files)
                meeting = FileMeeting(f, end_minutes) if f else None
            if meeting and not meeting.started:
                meeting.started = dt.datetime.now().isoformat(timespec="seconds")
                meeting.save()
                on_start(meeting, not args.no_session, not args.no_window)
        if meeting is not None:
            try:
                if not meeting.off():
                    meeting.step()
            except Exception as e:  # keep listening; the reason goes to the status log, never text
                status(f"pass failed: {type(e).__name__}: {str(e)[:150]}")
            if meeting.ended():
                if not meeting.off():
                    meeting.step()
                live_line(f"end {meeting.id} ({meeting.lines} lines{', switched off' if meeting.off() else ''})")
                status(f"meeting {meeting.id} ended, {meeting.lines} lines")
                if isinstance(meeting, FileMeeting):
                    done_files[str(meeting.path)] = meeting.path.stat().st_size if meeting.path.exists() else 0
                meeting = None
                if args.once:
                    lock.unlink(missing_ok=True)
                    return
        time.sleep(1 if meeting else 3)


def run_audio(args, cfg) -> None:
    """Mic + system sound, transcribed here with faster-whisper. Windows: WASAPI loopback via the soundcard package.
    Lightly tested on Windows only; system-audio capture on macOS needs an extra loopback driver and is untested."""
    import queue
    import threading
    import numpy as np
    import soundcard as sc
    from faster_whisper import WhisperModel

    sr, chunk_s = 16000, 8
    end_minutes = float(args.end_minutes or cfg["end_minutes"])
    lang = None if cfg["language"].lower() in ("auto", "") else cfg["language"][:2].lower()
    m = Meeting("audio-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
    m.started = dt.datetime.now().isoformat(timespec="seconds")
    m.save()
    print(f"Loading the {cfg['model']} speech model (first time downloads it)...", flush=True)
    model = WhisperModel(cfg["model"], device="auto", compute_type="auto")
    q: queue.Queue = queue.Queue()
    stop = threading.Event()

    def record(who: str, mic) -> None:
        with mic.recorder(samplerate=sr, channels=1) as rec:
            while not stop.is_set():
                q.put((who, dt.datetime.now(), rec.record(numframes=sr * chunk_s)[:, 0].astype(np.float32)))

    sources = [("me", sc.default_microphone())]
    try:
        sources.append(("others", sc.get_microphone(str(sc.default_speaker().name), include_loopback=True)))
    except Exception:
        print("System sound can't be captured here: only your microphone will be transcribed.", flush=True)
    for who, mic in sources:
        threading.Thread(target=record, args=(who, mic), daemon=True).start()
    on_start(m, not args.no_session, not args.no_window)
    print("Listening. Ctrl+C ends the meeting.", flush=True)
    try:
        while True:
            check_reminders(not args.no_window)
            if m.off() or (DATA / "stop").exists() or time.time() - m.last_new > end_minutes * 60:
                break
            try:
                who, at, audio = q.get(timeout=3)
            except queue.Empty:
                continue
            if float(np.abs(audio).max(initial=0)) < 0.005:
                continue  # silence
            segs, _ = model.transcribe(audio, language=lang, vad_filter=True, condition_on_previous_text=False)
            m.write([{"who": who, "wall": (at + dt.timedelta(seconds=s.start)).strftime("%H:%M:%S"),
                      "text": " ".join(s.text.split()), "_at": at + dt.timedelta(seconds=s.start)}
                     for s in segs if s.text.strip()])
    except KeyboardInterrupt:
        pass
    stop.set()
    (DATA / "stop").unlink(missing_ok=True)
    live_line(f"end {m.id} ({m.lines} lines)")
    status(f"meeting {m.id} ended (audio), {m.lines} lines")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="listen", choices=["listen", "audio"])
    ap.add_argument("--meetings-dir", help="Wispr meetings folder (default: Wispr's own)")
    ap.add_argument("--file", help="transcript file or folder (overrides settings.md, source = file)")
    ap.add_argument("--source", help="wispr | file (overrides settings.md)")
    ap.add_argument("--end-minutes", type=float, help="minutes of silence that end a meeting (overrides settings.md)")
    ap.add_argument("--no-session", action="store_true", help="don't start the Claude session (tests)")
    ap.add_argument("--no-window", action="store_true", help="don't open the cards window (tests)")
    ap.add_argument("--once", action="store_true", help="exit after the first meeting ends (tests)")
    args = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    cfg = settings()
    if args.source:
        cfg["source"] = args.source
    if args.mode == "audio":
        run_audio(args, cfg)
    else:  # with source = audio this only shows due reminders; meetings start with "listen.py audio"
        run_listener(args, cfg)


if __name__ == "__main__":
    if sys.stdout is not None:
        sys.stdout.reconfigure(encoding="utf-8")
    main()
`````

## File: `machete/cards.py`

`````python
"""Machete cards: the small always-on-top window where the meeting copilot offers things, and the CLI that fills it.

Nothing acts without a tap: ✓ makes the Machete session do exactly what the card says, ✕ drops it, OK closes an
information card. Each tap is written to data/live.log as "[machete] tap #<id> yes|no|ok: <text>", so the session
(watching that log) hears it within a second. On Windows 10 2004+ the window hides itself from screen sharing unless
the file data/show-on-share exists. Its own ✕ only hides the cards on screen: the next new card brings it back.

Cards are read at a glance mid-conversation: a big bold headline (first line), at most two short lines under it,
the source small and grey. Write "\\n" for a new line.

Usage (from the kit folder):
    python machete/cards.py window                                   # the window (one at a time)
    python machete/cards.py add <kind> "<headline>\\n<line>\\n<line>" [--source "<where from>"] [--meeting <id>]
                   [--link "<label>|<target>"]...                     # prints the new card's id
        Links (up to 3, a click opens them and is not a tap): https://..., mailto:..., slack://..., or an existing
        local file or folder (never a program or script).
    python machete/cards.py done <id> "<what was done>"   # shows "✓ ..." on it for a while, then it goes
    python machete/cards.py drop <id>                     # removes an open card
    python machete/cards.py clear [--keep-meeting <id>]   # drops open cards of other meetings
    python machete/cards.py list [--open]                 # JSON
Kinds: answer, headsup, date, slots (find a time), task, person, fact, timezone, prep, followup, reminder, consent, list, other.
Information only (one OK button): answer, headsup, person, fact, timezone, prep, reminder, consent, list.
Store: data/cards.jsonl (append-only events).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import platform
import socket
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import DATA as LIVE  # noqa: E402

STORE = LIVE / "cards.jsonl"
LOG = LIVE / "live.log"
ICON = {"answer": "🔎", "headsup": "⚡", "heads-up": "⚡", "date": "📅", "slots": "🗓️", "task": "✅", "person": "👤", "fact": "🔢", "timezone": "🌐", "prep": "🗂️",
        "followup": "✉️", "reminder": "⏰", "consent": "🎙️", "list": "📋", "other": "💡"}
INFO_ONLY = {"answer", "headsup", "heads-up", "person", "fact", "timezone", "prep", "reminder", "consent", "list"}
SHOW_DONE = 25  # seconds a done card stays visible
MAX_LINES = 3   # headline + 2
MAX_LINKS = 3
IS_WIN = platform.system() == "Windows"

BG, CARD, FG, DIM, ACCENT = "#17171c", "#26262e", "#f1f3f4", "#9aa0a6", "#8ab4f8"
FONT = "Segoe UI" if IS_WIN else "Helvetica"


def events() -> list[dict]:
    try:
        return [json.loads(l) for l in STORE.read_text(encoding="utf-8").splitlines() if l.strip()]
    except FileNotFoundError:
        return []


def append(ev: dict) -> None:
    LIVE.mkdir(parents=True, exist_ok=True)
    ev["at"] = time.time()
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def cards() -> dict[int, dict]:
    out: dict[int, dict] = {}
    for e in events():
        if e["op"] == "add":
            out[e["id"]] = {"id": e["id"], "kind": e["kind"], "text": e["text"], "source": e.get("source"),
                            "links": e.get("links") or [], "meeting": e.get("meeting"), "added": e["at"],
                            "state": "open", "result": None, "closed": None}
        elif e["id"] in out:
            c = out[e["id"]]
            if e["op"] == "tap":
                c.update(state="tapped-" + e["answer"], closed=e["at"])
            elif e["op"] == "done":
                c.update(state="done", result=e.get("result"), closed=e["at"])
            elif e["op"] == "drop":
                c.update(state="dropped", closed=e["at"])
    return out


def live_line(text: str) -> None:
    LIVE.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} [machete] {' '.join(text.split())}\n")


def card_lines(text: str) -> list[str]:
    lines = [l.strip() for l in text.replace("\\n", "\n").split("\n") if l.strip()]
    return lines[:MAX_LINES] or [""]


SCHEMES = ("https://", "http://", "slack://", "mailto:", "notion://", "msteams:")
NO_RUN = {".exe", ".bat", ".cmd", ".com", ".ps1", ".psm1", ".vbs", ".vbe", ".js", ".jse", ".wsf", ".wsh", ".msi",
          ".msp", ".scr", ".lnk", ".url", ".py", ".pyw", ".reg", ".hta", ".cpl", ".jar", ".appref-ms", ".sh",
          ".command", ".app"}


def link_target(target: str) -> str | None:
    """What a card link opens, or None if not allowed: web, mail, Slack, Notion and Teams links, or an existing
    local file or folder that isn't a program or script (a click opens things, it never runs them)."""
    t = target.strip()
    if t.lower().startswith(SCHEMES):
        return t if not any(ch in t for ch in "\r\n\t") else None
    p = pathlib.Path(os.path.expanduser(t))
    if p.is_absolute() and p.exists() and (p.is_dir() or p.suffix.lower() not in NO_RUN):
        return str(p)
    return None


def open_url(url: str) -> None:
    if IS_WIN:
        os.startfile(url)  # type: ignore[attr-defined]
    elif platform.system() == "Darwin":
        __import__("subprocess").Popen(["open", url])
    else:
        __import__("subprocess").Popen(["xdg-open", url])


OPEN = open_url  # tests swap this out


def link_icon(url: str) -> str:
    u = url.lower()
    if u.startswith("slack://") or ".slack.com/" in u:
        return "💬"
    if "calendar.google.com" in u or "outlook.office" in u:
        return "📅"
    if u.startswith("mailto:") or "mail.google.com" in u:
        return "✉️"
    if u.startswith(("https://", "http://", "notion://", "msteams:")):
        return "🌐"
    return "📁"


def parse_links(a: list[str]) -> list[dict]:
    out = []
    for i, x in enumerate(a):
        if x == "--link" and i + 1 < len(a) and "|" in a[i + 1]:
            label, target = a[i + 1].split("|", 1)
            url = link_target(target)
            if url and label.strip():
                out.append({"label": " ".join(label.split())[:28], "url": url})
            else:
                print(f"link skipped (not allowed or not found): {a[i + 1][:80]}", file=sys.stderr)
    return out[:MAX_LINKS]


def cmd_add(kind: str, text: str, meeting: str | None, source: str | None, links: list[dict] | None = None) -> int:
    new_id = max(cards(), default=0) + 1
    append({"op": "add", "id": new_id, "kind": kind if kind in ICON else "other",
            "text": "\n".join(card_lines(text))[:300], "source": (source or "")[:120] or None, "meeting": meeting,
            "links": links or []})
    return new_id


def work_area(root) -> tuple[int, int, int, int]:
    """The usable screen area (left, top, right, bottom), above the Windows taskbar where possible."""
    if IS_WIN:
        try:
            import ctypes
            from ctypes import wintypes
            r = wintypes.RECT()
            ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(r), 0)  # SPI_GETWORKAREA
            return r.left, r.top, r.right, r.bottom
        except Exception:
            pass
    return 0, 0, root.winfo_screenwidth(), root.winfo_screenheight() - 60


LOGO_RED = "#E5322D"
LOGO_FOLD = 28  # hand units the index sits lower when folded: only its rounded tip shows, as a fourth knuckle
# The index's offset, one frame each: folded, a small dip, then it slides straight up out of the fist and settles.
LOGO_RAISE = (28, 28, 30, 31, 24, 13, 3, -4, -5, -2, 1, 0)


def logo_shapes(size: float, lift: float = 0.0, ink: str = "#F4EFE4") -> list[tuple[list[float], str]]:
    """The small mark (assets/machete-logo-small.svg) as canvas polygons, back to front: index finger, fist, red cuff.
    lift: how far down the index sits, in hand units (0 = raised, LOGO_FOLD = folded behind the fist).
    The finger only slides; nothing is ever scaled or rotated. The fist is drawn over it, so its base stays covered."""
    import math
    k = size / 120

    def arc(cx: float, cy: float, r: float, a0: float, a1: float, n: int = 8) -> list[tuple[float, float]]:
        return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

    def cubic(p0, p1, p2, p3, n: int = 10) -> list[tuple[float, float]]:
        return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d
                      for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(1, n + 1))]

    def pill(left: float, top: float, right: float, bottom: float, r: float) -> list[tuple[float, float]]:
        return (arc(left + r, top + r, r, 180, 270) + arc(right - r, top + r, r, 270, 360)
                + arc(right - r, bottom - r, r, 0, 90) + arc(left + r, bottom - r, r, 90, 180))

    def hand(pts: list[tuple[float, float]]) -> list[float]:  # hand units -> mark units -> pixels
        return [v for x, y in pts for v in ((9 + .82 * x - 1) * k, (2 + .82 * y - 2) * k)]

    index = pill(42, 6 + lift, 60, 82 + lift, 9)
    fist = ([(42, 52), (60, 52)] + arc(69, 47, 9, 180, 360) + arc(86.5, 52.5, 8.5, 180, 360)
            + arc(102.5, 59.5, 7.5, 180, 360) + [(110, 84)] + cubic((110, 84), (110, 104), (96, 114), (78, 114))
            + [(56, 114)] + cubic((56, 114), (46, 114), (37, 108), (32.8, 99.4))
            + arc(24, 62, 8, 154.7, 334.7) + [(40, 77.5), (41.6, 79.5), (42, 75)])
    cuff = [v for x, y in pill(42, 101, 92, 117, 5.5) for v in ((x - 1) * k, (y - 2) * k)]
    return [(hand(index), ink), (hand(fist), ink), (cuff, LOGO_RED)]


def draw_logo(canvas, size: int, lift: float = 0.0) -> None:
    canvas.delete("all")
    for points, colour in logo_shapes(size, lift):
        canvas.create_polygon(points, fill=colour, outline="")


def window(capturable: bool = False, on_ready=None) -> None:
    """capturable=True: a copy screenshots can see (tests). on_ready(root, frame): called once drawn (tests)."""
    if IS_WIN:
        try:  # real pixels, so the position matches the screen at any Windows scaling
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    import tkinter as tk
    try:  # one window at a time
        guard = socket.socket()
        guard.bind(("127.0.0.1", 47382 if capturable else 47381))
    except OSError:
        return
    root = tk.Tk()
    root.withdraw()
    root.title("Machete (test)" if capturable else "Machete")
    root.overrideredirect(True)  # no title bar: its own small ✕, dragged by the cards
    root.attributes("-topmost", True)
    root.configure(bg=BG)
    root.resizable(False, False)
    root.update_idletasks()
    if IS_WIN:
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
            dwm = ctypes.windll.dwmapi
            for attr, value in ((33, 2), (34, 0x00463C3A), (2, 2)):  # round corners, faint edge, shadow on
                v = ctypes.c_int(value)
                dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(v), 4)

            class MARGINS(ctypes.Structure):
                _fields_ = [("l", ctypes.c_int), ("r", ctypes.c_int), ("t", ctypes.c_int), ("b", ctypes.c_int)]
            dwm.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 1, 1)))
            # Hidden from screen shares (WDA_EXCLUDEFROMCAPTURE) unless data/show-on-share exists.
            if not capturable and not (LIVE / "show-on-share").exists():
                ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x11)
        except Exception:
            pass
    frame = tk.Frame(root, bg=BG, padx=10, pady=6)
    frame.pack(fill="both")
    shown: list = [None]
    hidden_upto: list = [None]
    moved: list = [None]
    grab = {"x": 0, "y": 0}
    WIDTH = 400
    LOGO = 26  # px, the mark in the header
    newest: list = [max(cards(), default=0)]  # a card above this id is new: the finger goes up
    root.logo_plays = 0  # tests read this
    root.logo_lift = 0

    def play_logo(canvas, frame_no: int = 0) -> None:
        if not canvas.winfo_exists():  # the header was redrawn meanwhile
            return
        root.logo_lift = LOGO_RAISE[frame_no]  # tests read this
        draw_logo(canvas, LOGO, LOGO_RAISE[frame_no])
        if frame_no + 1 < len(LOGO_RAISE):
            root.after(40, play_logo, canvas, frame_no + 1)

    def drag_start(e) -> None:
        grab.update(x=e.x_root - root.winfo_x(), y=e.y_root - root.winfo_y())

    def drag_move(e) -> None:
        x, y = e.x_root - grab["x"], e.y_root - grab["y"]
        root.geometry(f"+{x}+{y}")
        moved[0] = (x + root.winfo_width(), y + root.winfo_height())

    def draggable(w) -> None:
        if isinstance(w, tk.Button) or hasattr(w, "_link"):
            return
        w.bind("<ButtonPress-1>", drag_start)
        w.bind("<B1-Motion>", drag_move)
        for ch in w.winfo_children():
            draggable(ch)

    def follow(c: dict, ln: dict) -> None:
        url = link_target(ln["url"])  # checked again: the store is a plain file
        wlog(f"link #{c['id']}: {'opened' if url else 'refused'}")
        if url:
            try:
                OPEN(url)
            except OSError as e:
                wlog(f"link #{c['id']} failed: {type(e).__name__}")

    def tap(c: dict, answer: str) -> None:
        append({"op": "tap", "id": c["id"], "answer": answer})
        live_line(f"tap #{c['id']} {answer}: {' / '.join(card_lines(c['text']))[:120]}")
        draw(force=True)

    def button(parent, text: str, cmd, primary: bool = False):
        return tk.Button(parent, text=text, command=cmd, font=(FONT, 12, "bold"), width=4, relief="flat",
                         cursor="hand2", bg=ACCENT if primary else "#3c3c46", fg="#111111" if primary else FG,
                         activebackground=ACCENT, bd=0, padx=6, pady=2)

    def draw(force: bool = False) -> None:
        now = time.time()
        visible = [c for c in cards().values()
                   if c["state"] == "open" or (c["state"] == "done" and now - (c["closed"] or 0) < SHOW_DONE)]
        if hidden_upto[0] is not None:
            visible = [c for c in visible if c["id"] > hidden_upto[0]]
        visible = sorted(visible, key=lambda c: c["id"])[-4:]
        key = [(c["id"], c["state"]) for c in visible]
        if key == shown[0] and not force:
            return
        shown[0] = key
        for w in frame.winfo_children():
            w.destroy()
        if not visible:
            root.withdraw()
            return
        bar = tk.Frame(frame, bg=BG)
        bar.pack(fill="x")
        mark = tk.Canvas(bar, width=LOGO, height=LOGO, bg=BG, highlightthickness=0, bd=0)
        mark.pack(side="left", padx=(0, 0))
        tk.Label(bar, text="Machete", bg=BG, fg=DIM, font=(FONT, 9)).pack(side="left", padx=(2, 0))
        top = max(c["id"] for c in visible)
        if top > newest[0]:  # a new card landed
            newest[0] = top
            root.logo_plays += 1
            draw_logo(mark, LOGO, LOGO_FOLD)  # a fist first, then the finger slides up
            root.after(120, play_logo, mark)
        else:
            draw_logo(mark, LOGO)
        x = tk.Button(bar, text="✕", command=closed, font=(FONT, 10), relief="flat", bd=0, cursor="hand2", padx=6,
                      pady=0, bg=BG, fg=DIM, activebackground="#3c3c46", activeforeground=FG)
        x.pack(side="right")
        for c in visible:
            box = tk.Frame(frame, bg=CARD, padx=12, pady=10)
            box.pack(fill="x", pady=4)
            lines = card_lines(c["text"])
            head = tk.Frame(box, bg=CARD)
            head.pack(fill="x", anchor="w")
            tk.Label(head, text=ICON.get(c["kind"], "💡"), bg=CARD, fg=FG, font=(FONT, 16)).pack(side="left", anchor="n")
            tk.Label(head, text=lines[0], bg=CARD, fg=FG, font=(FONT, 15, "bold"), wraplength=WIDTH - 60,
                     justify="left").pack(side="left", anchor="w", padx=(8, 0))
            for line in lines[1:]:
                tk.Label(box, text=line, bg=CARD, fg=FG, font=(FONT, 13), wraplength=WIDTH - 30,
                         justify="left").pack(anchor="w", pady=(4, 0))
            if c.get("links"):
                row_l = tk.Frame(box, bg=CARD)
                row_l.pack(anchor="w", pady=(6, 0))
                for ln in c["links"][:MAX_LINKS]:
                    lab = tk.Label(row_l, text=f"{link_icon(ln['url'])} {ln['label']}", bg=CARD, fg=ACCENT,
                                   font=(FONT, 10), cursor="hand2")
                    lab._link = ln
                    lab.bind("<Button-1>", lambda e, c=c, ln=ln: follow(c, ln))
                    lab.pack(side="left", padx=(0, 12))
            if c.get("source"):
                tk.Label(box, text=c["source"], bg=CARD, fg=DIM, font=(FONT, 9), wraplength=WIDTH - 30,
                         justify="left").pack(anchor="w", pady=(6, 0))
            if c["state"] == "done":
                tk.Label(box, text=f"✓ {c['result'] or 'Done'}", bg=CARD, fg=ACCENT, font=(FONT, 12, "bold"),
                         wraplength=WIDTH - 30, justify="left").pack(anchor="w", pady=(6, 0))
                continue
            row = tk.Frame(box, bg=CARD)
            row.pack(anchor="e", pady=(8, 0))
            if c["kind"] in INFO_ONLY:
                button(row, "OK", lambda c=c: tap(c, "ok")).pack(side="right")
            else:
                button(row, "✕", lambda c=c: tap(c, "no")).pack(side="right", padx=(6, 0))
                button(row, "✓", lambda c=c: tap(c, "yes"), primary=True).pack(side="right")
        draggable(frame)
        root.update_idletasks()
        place()
        root.deiconify()
        root.attributes("-topmost", True)

    def place() -> None:
        root.update_idletasks()
        w, h = WIDTH + 20, frame.winfo_reqheight()
        left, top, right, bottom = work_area(root)
        r, b = moved[0] or (right - 16, bottom - 16)
        r, b = min(max(r, left + w), right), min(max(b, top + h), bottom)
        root.geometry(f"{w}x{h}+{r - w}+{b - h}")

    def wlog(text: str) -> None:
        try:
            with (LIVE / "window.log").open("a", encoding="utf-8") as f:
                f.write(f"{dt.datetime.now().isoformat(timespec='seconds')} {text}\n")
        except OSError:
            pass

    def closed() -> None:
        hidden_upto[0] = max(cards(), default=0)
        wlog(f"hidden (cards up to #{hidden_upto[0]})")
        shown[0] = None
        root.withdraw()

    root.protocol("WM_DELETE_WINDOW", closed)
    wlog("opened")

    def tick() -> None:
        try:
            draw()
        finally:
            root.after(1000, tick)

    tick()
    if on_ready:
        root.after(1500, lambda: on_ready(root, frame))
    root.mainloop()


def opt(a: list[str], name: str) -> str | None:
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else None


def main(a: list[str]) -> None:
    if not a:
        print(__doc__); return
    if a[0] == "window":
        window(capturable="--capturable" in a)
    elif a[0] == "add" and len(a) >= 3:
        print(cmd_add(a[1], a[2], opt(a, "--meeting"), opt(a, "--source"), parse_links(a)))
    elif a[0] == "done" and len(a) >= 2:
        append({"op": "done", "id": int(a[1]), "result": (a[2] if len(a) > 2 else "")[:200]}); print("ok")
    elif a[0] == "drop" and len(a) >= 2:
        append({"op": "drop", "id": int(a[1])}); print("ok")
    elif a[0] == "clear":
        keep = opt(a, "--keep-meeting")
        gone = [c["id"] for c in cards().values() if c["state"] == "open" and c.get("meeting") != keep]
        for i in gone:
            append({"op": "drop", "id": i})
        print(f"dropped {len(gone)}")
    elif a[0] == "list":
        cs = [c for c in cards().values() if "--open" not in a or c["state"] == "open"]
        print(json.dumps(cs, ensure_ascii=False, indent=1))
    else:
        print(__doc__)


if __name__ == "__main__":
    if sys.stdout is not None:
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
`````

## File: `machete/follow.py`

`````python
"""Prints each new line of a text file that contains a marker, as it is appended (a portable `tail -F | grep`).

The Machete session's Monitor runs this on data/live.log. It polls the file size every half second, starts at the
current end of the file, survives the file being missing or truncated, and exits after --seconds (default 1800).

Usage:  python -u machete/follow.py data/live.log [--marker "[machete] "] [--seconds 1800]
"""
from __future__ import annotations

import os
import sys
import time


def main(a: list[str]) -> int:
    if not a:
        print(__doc__)
        return 2
    path = a[0]
    marker = a[a.index("--marker") + 1] if "--marker" in a else "[machete] "
    limit = float(a[a.index("--seconds") + 1]) if "--seconds" in a else 1800.0
    end = time.time() + limit
    try:
        pos = os.path.getsize(path)
    except OSError:
        pos = 0
    rest = b""
    while time.time() < end:
        try:
            size = os.path.getsize(path)
        except OSError:
            time.sleep(0.5)
            continue
        if size < pos:
            pos, rest = 0, b""
        if size > pos:
            with open(path, "rb") as f:
                f.seek(pos)
                chunk = f.read(size - pos)
            pos = size
            lines = (rest + chunk).split(b"\n")
            rest = lines.pop()
            for raw in lines:
                line = raw.decode("utf-8", errors="replace").rstrip("\r")
                if marker in line:
                    sys.stdout.write(line + "\n")
                    sys.stdout.flush()
        time.sleep(0.5)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
`````

## File: `machete/remind.py`

`````python
"""Local reminders: the fallback when you have no task tool connected to Claude.

A reminder is a line in data/reminders.jsonl. The background listener checks every few seconds and, when one is
due, shows it as a card in the Machete window. Nothing leaves this PC. The PC has to be on and the listener running.

Usage (from the kit folder):
    python machete/remind.py add "YYYY-MM-DD HH:MM" "Send Sam the Q3 proposal"   # local time
    python machete/remind.py list
    python machete/remind.py cancel <id>
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import DATA  # noqa: E402

STORE = DATA / "reminders.jsonl"


def load() -> list[dict]:
    try:
        return [json.loads(l) for l in STORE.read_text(encoding="utf-8").splitlines() if l.strip()]
    except FileNotFoundError:
        return []


def save(items: list[dict]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    STORE.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in items), encoding="utf-8")


def fire_due() -> int:
    """Shows every due reminder as a card; returns how many."""
    items, now, fired = load(), dt.datetime.now(), 0
    for r in items:
        if not r.get("fired") and dt.datetime.fromisoformat(r["when"]) <= now:
            subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("cards.py")), "add", "reminder",
                            r["text"], "--source", f"Reminder set for {r['when'][:16].replace('T', ' ')}"],
                           capture_output=True)
            r["fired"], fired = True, fired + 1
    if fired:
        save(items)
    return fired


def main(a: list[str]) -> None:
    if len(a) >= 3 and a[0] == "add":
        when = dt.datetime.strptime(a[1], "%Y-%m-%d %H:%M")
        items = load()
        new_id = max((r["id"] for r in items), default=0) + 1
        items.append({"id": new_id, "when": when.isoformat(), "text": a[2][:200], "fired": False})
        save(items)
        print(f"reminder {new_id} set for {when:%a %d %b %H:%M}")
    elif a[:1] == ["list"]:
        for r in load():
            print(f"{r['id']}  {r['when'][:16]}  {'(shown) ' if r['fired'] else ''}{r['text']}")
    elif len(a) >= 2 and a[0] == "cancel":
        save([r for r in load() if str(r["id"]) != a[1]])
        print("ok")
    else:
        print(__doc__)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
`````

## File: `machete/fake_meeting.py`

`````python
"""A fake meeting, so Machete can be tried and tested without a real call.

    python machete/fake_meeting.py --check
        End-to-end test in a temporary folder: plays the script below in Wispr's format and as a plain text file,
        runs the listener on each (no Claude session, no window), and checks the transcript lines, the start and end
        lines and the consent card. Prints PASS or FAIL. Touches nothing outside the temporary folder.

    python machete/fake_meeting.py --play wispr --dir data/fake-meetings [--speed 2]
    python machete/fake_meeting.py --play file  --dir data/fake-meetings [--speed 2]
        Plays the script in real time into --dir, for a live demo: run the listener on the same folder
        (python machete/listen.py --meetings-dir data/fake-meetings, or --source file --file data/fake-meetings)
        and the Claude session starts and offers cards as if it were a call.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent

SCRIPT = [  # (seconds from start, who, text)
    (0, "others", "Hi everyone, thanks for joining. Let's go through the Q3 proposal."),
    (4, "me", "Sounds good. I shared the draft with the designer yesterday."),
    (9, "others", "Great. Sam will want the updated budget before the client call."),
    (14, "me", "I'll send Sam the updated numbers by Friday."),
    (19, "others", "Can we meet again Thursday at 3 pm Eastern to review it?"),
    (24, "me", "Thursday works for me."),
    (28, "others", "What was the total we quoted them last time?"),
    (33, "me", "I'll check. Let's wrap up here, thanks all."),
]


def play(mode: str, out_dir: pathlib.Path, speed: float, quiet: bool = False) -> pathlib.Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%H%M%S")
    t0 = time.time()
    if mode == "wispr":
        folder = out_dir / f"fake-{stamp}"
        folder.mkdir()
        target = folder / "live.ndjson"
    else:
        folder = out_dir
        target = out_dir / f"fake-transcript-{stamp}.txt"
    if not quiet:
        print(f"playing the fake meeting into {target}", flush=True)
    for i, (at, who, text) in enumerate(SCRIPT):
        while time.time() - t0 < at / speed:
            time.sleep(0.1)
        with target.open("a", encoding="utf-8") as f:
            if mode == "wispr":
                now = int(time.time() * 1000)
                f.write(json.dumps({"id": f"seg-{i}", "text": text, "startEpochMs": now,
                                    "speaker": {"source": "mic" if who == "me" else "system"}}) + "\n")
            else:
                f.write(f"{'Me' if who == 'me' else 'Alex'}: {text}\n")
    if mode == "wispr":
        time.sleep(2)
        (folder / "upload.ogg").write_bytes(b"")  # what Wispr writes when recording stops
    if not quiet:
        print("done", flush=True)
    return target


def check() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        for mode in ("wispr", "file"):
            data = pathlib.Path(tmp) / f"data-{mode}"
            meetings = pathlib.Path(tmp) / f"meetings-{mode}"
            meetings.mkdir()
            env = dict(os.environ, MACHETE_DATA=str(data), PYTHONIOENCODING="utf-8")
            args = [sys.executable, str(HERE / "listen.py"), "--source", mode, "--no-session", "--no-window", "--once",
                    "--end-minutes", "0.15"]
            args += ["--meetings-dir", str(meetings)] if mode == "wispr" else ["--file", str(meetings)]
            listener = subprocess.Popen(args, env=env)
            play(mode, meetings, speed=8, quiet=True)
            try:
                listener.wait(timeout=60)
            except subprocess.TimeoutExpired:
                listener.kill()
            log = (data / "live.log").read_text(encoding="utf-8") if (data / "live.log").exists() else ""
            said = [l for l in log.splitlines() if "[machete] @" in l]
            card_list = subprocess.run([sys.executable, str(HERE / "cards.py"), "list"], env=env, capture_output=True,
                                       text=True, encoding="utf-8").stdout
            checks = {
                "start line": "[machete] start " in log,
                f"{len(SCRIPT)} transcript lines": len(said) == len(SCRIPT),
                "me / others labels": any("@me:" in l for l in said) and any(("@others:" in l or "@Alex:" in l)
                                                                            for l in said),
                "end line": "[machete] end " in log,
                "consent card": '"kind": "consent"' in card_list,
            }
            for name, passed in checks.items():
                print(f"  {mode:5} {'ok  ' if passed else 'FAIL'} {name}")
                ok &= passed
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--play", choices=["wispr", "file"])
    ap.add_argument("--dir", default="data/fake-meetings")
    ap.add_argument("--speed", type=float, default=1)
    a = ap.parse_args()
    if a.check:
        return check()
    if a.play:
        play(a.play, pathlib.Path(a.dir), a.speed)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
`````

## File: `machete/session-prompt.md`

`````markdown
# Machete: the meeting copilot session

You are **Machete**, a live meeting copilot for the person who owns this computer ("the user"). You run in a Claude
Code session started by `machete/listen.py` when a meeting starts. Run every command from the kit folder (your working
directory). A local listener writes the meeting, line by line, to `data/live.log`. Your job: notice the few moments
where you can save the user a step and offer them as cards in a small window on their screen.
**Nothing acts without a ✓ tap.**

## Start
1. Read `settings.md`: the user's name, tools, where to look things up, meetings to skip, card rules, language.
2. Load the Monitor tool (ToolSearch "select:Monitor") and see which connectors you have (calendar, mail, chat, tasks,
   CRM, sheets, docs). Use only what is connected; never ask the user to connect anything mid-meeting.
3. **What meeting is this?** If a calendar connector exists, find the event happening now.
   - **Private: switch off before reading anything.** If the event matches "Meetings to skip" (a listed keyword in
     its title or description, private visibility) or the settings say to skip meetings with no event: create the
     empty file `data/<meeting id>/off`, run `python machete/cards.py list --open` and `drop` this meeting's cards,
     say one line, and end. Read no transcript.
   - Otherwise note the attendees, the title and the invite's description and links.
4. **Prep card** (if "prep at start" is on and there is an event): one information card with who's on the call and the
   one or two things worth remembering (last notes about them or the topic from the notes folder / CRM / docs, open
   items). Kind `prep`. Example: `Q3 review · Sam, Alex\nLast time: budget open\nSam owes the draft`. Skip it if you
   find nothing useful.
5. Catch up on anything already said: read `data/<meeting id>/segments.jsonl` if it exists.
6. Arm the Monitor (below) and wait silently.

## The Monitor
Monitor tool, description `Machete: meeting transcript`, timeout_ms 1800000; re-arm it when it expires until the
meeting ends:

```
python -u machete/follow.py data/live.log --seconds 1800
```

Lines look like `2026-03-12T14:03:12 [machete] @others: let's meet Thursday at 3 pm Eastern` (`@me` = the user's mic,
`@others` or a name = the call), `[machete] tap #4 yes|no|ok: <card text>`, `[machete] start <id>`,
`[machete] end <id> (...)`. The transcript is a few seconds behind, comes in short pieces and makes mistakes,
names above all: check a name against the user's notes, the invite or the CRM before trusting it.

## Cards
`python machete/cards.py add <kind> "<headline>\n<line>\n<line>" --source "<where from>" --meeting <id>`
(prints the card id). Up to 3 links: `--link "<label>|<https://... or mailto:... or a local file/folder>"`.
- The **headline** is the answer or the action in 2 to 5 words; it shows big. At most two short lines under it, only
  if they help act. The source goes in `--source`, never in the text. The meeting's language unless settings say
  otherwise.
- **Link the source, every time there is one.** Any card built from something you read gets `--link` to it: the
  email thread, the doc, the sheet, the CRM record, the calendar event, the web page (up to 3, best first; label 1 to
  3 words, never the raw URL). The user should be able to open the proof with one click while they talk.

**Use judgment, not a trigger list.** You are a sharp colleague sitting next to the user, reading the whole
conversation and the user's world (their sources, connectors and the web). The one question every time: *what would
help the user most in this moment, that they don't have in front of them?* The kinds below are labels and examples
of shapes a card can take, not a list to match against. Invent the card the moment needs: the open item nobody
raised, a number that doesn't match the records, "that deck from October" as a link, the question the user was just
asked while looking away, "what have we agreed so far?" from this transcript, an absent person's availability, date
math with holidays, money at today's rate, a past decision that contradicts this one, and anything else of that
calibre. If no kind fits, use `other`. The limits that never bend: nothing acts without ✓, rare, never filler,
never a guess, a source and link for anything you read.

Kinds (only those on in settings; examples, not limits):
- **heads-up** ⚡ Nobody asked, but something the meeting is talking about has a fact the user would want right now,
  and that the room may not know: a reply that arrived minutes ago in the thread being discussed, a deadline or due
  invoice for the client on the call, a clash with something already promised, today's news about the company or
  product being discussed, a changed price or policy on a public page. Also what's **relevant but missing**:
  something that bears on the topic and that nobody has mentioned and that isn't in the meeting notes or agenda,
  e.g. an open item or promise from the last meeting with these people that hasn't come up, a document or thread
  about exactly this topic that nobody has referenced, a past decision that contradicts what's being decided now, a
  number said in the meeting that doesn't match the user's records. Card: `Acme replied 10 min ago\nThey accepted
  the March start` with `--source "your email"` and a link to it. Only when it clearly matters to what is being
  decided now, at most about one every 10 minutes, never a guess, never filler. Check quietly as topics come up
  (one quick lookup in the user's sources, then the web if on); no card if nothing important turns up.
- **date** 📅 A date or time said for something to happen. Work out the exact date and time and check the calendar
  for a clash. `Thu 12 Mar · 15:00\nQ3 review with Sam\nAdd it? You're free` (or `Clashes with team sync`).
  ✓ = create the event in the user's calendar (no invitations sent to others).
- **slots** 🗓️ Someone says "let's find a time for all of us". Read the calendars you can see through the calendar
  connector (the user's, and attendees' free/busy if the connector shows it), within the work hours in settings, and
  offer 2 or 3 free slots: `Free: Tue 10:00 · Wed 15:30\nAll 4 attendees free\nDraft them as options?`.
  ✓ = put the slots in an email or chat draft to the attendees (never sent), or, if the card said so, create a
  tentative hold on the user's own calendar. Never send invitations.
- **timezone** 🌐 A time said in another zone ("3 pm Eastern", "10 am London"). `3 pm ET = 17:00 yours\nSam: 3 pm`.
  Information only.
- **task** ✅ A clear commitment by the user ("I'll send Sam the numbers by Friday"). `Send Sam the numbers\nFri 10:00
  in Asana?`. ✓ = create it in the task tool from settings through its connector; **if there is no task connector,
  a local reminder on this computer**: `python machete/remind.py add "YYYY-MM-DD HH:MM" "<task>"` (it pops up as a card
  at that time while the listener runs). Say which in the card (`Remind you Fri 10:00?`).
- **answer** 🔎 **The most valuable card: do these first.** Someone in the meeting asks a question, or the
  conversation stalls on something nobody knows ("what did we quote them?", "did they ever reply?", "how many signed
  up?", "what does the contract say about cancelling?", "how big is their team?", "what does their tool cost?").
  Find the answer while the question is still open and show it, with where it came from:
  - the user's own sources first, through their connectors and files: email, docs and Drive, sheets, the CRM, the
    task tool, the calendar, the notes folder;
  - then, if `Web lookups` is on in settings, the web for public facts (a company, a product, a price, a law, a
    definition), with the page as the source.
  Card: `Quoted: $48,000\nProposal v2, sent 3 Feb` with `--source "Q3 proposal (Drive)"` and a link to it. Give the
  answer itself, not "I found a document". Not sure or not found: no card (note it on the end-of-meeting list).
  Information only. A direct question may get its card at any time (the 2-minute spacing below doesn't hold it back),
  but never answer the same question twice. Speed matters: one or two targeted lookups, not a long research session;
  if it needs more, put "look into X" on the end-of-meeting list.
- **person** 👤 Someone is mentioned who has a note in the user's notes or the CRM, and one fact would help now.
  `Sam Lee · Acme, finance\nPrefers numbers by email`. From the notes, never guessed. Information only.
- **other** 💡 Rarely: anything else clearly useful with one tap.

**Keep it rare** (and follow "Card rules" in settings): nothing in the first 2 minutes except the prep card and answers, at most
one card every 2 minutes and about 6 an hour, never the same thing twice, only with a clear trigger plus a confirming
sign (a future date, a known name, the user speaking or being spoken to). Anything less sure goes on the
end-of-meeting list: append `{"kind","text","why"}` to `data/<meeting id>/candidates.jsonl`.

## Taps
- `yes`: do exactly what the card said and nothing more, then `python machete/cards.py done <id> "<what you did>"`
  (e.g. `Added to Calendar`). If it can't be done: `done <id> "Couldn't: <why>"`.
- `no` and `ok`: nothing.

## Privacy (never break these)
- The transcript goes nowhere but this session. The only thing that goes out is the single action the user tapped
  ✓ (an event, a task, a draft), with only the words that action needs. Never paste transcript text into any other
  tool, chat or document. Reading the user's own calendar, notes, CRM, mail or docs to prepare a card is fine.
- Web lookups (only if on in settings): short, neutral queries about public things (a company, product, price, law,
  term). Never put quotes from the meeting, people's private details or anything confidential into a web search.
- Drafts only: never send an email or chat message, never invite people.
- Keep sensitive details (health, money, personal life) out of cards.
- Write no transcript anywhere outside `data/`.

## When the meeting ends (`[machete] end <id>`)
1. **Follow-up email** (if on and the meeting had other people): draft a short follow-up into the user's email drafts
   through the mail connector (to the attendees from the invite; decisions, who does what, dates). Never send it. No
   mail connector: write it to `data/<meeting id>/follow-up.md`.
2. Write `data/<meeting id>/report.md`: the meeting, the cards offered and what happened to each, and the
   end-of-meeting list from candidates.jsonl as a short checklist. No transcript.
3. Drop this meeting's cards still open (`cards.py list --open`, then `drop <id>`), then add one card `list`
   `End-of-meeting list\n<n> items · follow-up drafted` with `--link "Report|<absolute path of report.md>"`.
4. Stop the Monitor (TaskStop), say one line, and stay idle. The next meeting gets a fresh session.
`````

## File: `machete/start_session.ps1`

`````powershell
# Starts the Machete Claude Code session for one meeting in its own terminal window (Windows).
# Called by listen.py when a meeting starts. A previous Machete session is closed first, so each meeting starts
# with a fresh context.
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\start_session.ps1 -Meeting <meeting id>
param([string]$Meeting = '')

$kit = Split-Path -Parent $PSScriptRoot
$title = 'Machete meeting copilot'
Get-CimInstance Win32_Process -Filter "name='claude.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*$title*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) { $claude = Join-Path $env:USERPROFILE '.local\bin\claude.exe' }
$prompt = "Read machete/session-prompt.md and follow it. The meeting that just started has the id $Meeting."
$inner = Join-Path $env:TEMP 'machete-session.ps1'
@"
`$Host.UI.RawUI.WindowTitle = '$title'
Set-Location '$kit'
& '$claude' --name '$title' -- "$prompt"
"@ | Set-Content -Path $inner -Encoding utf8

$wt = Get-Command wt.exe -ErrorAction SilentlyContinue
if ($wt) {
    & wt.exe -w machete new-tab --title 'Machete' -d $kit powershell -NoProfile -NoExit -ExecutionPolicy Bypass -File $inner
} else {
    Start-Process powershell -ArgumentList '-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $inner -WorkingDirectory $kit
}
`````

## File: `machete/start_session.sh`

`````sh
#!/bin/sh
# Starts the Machete Claude Code session for one meeting in a new terminal window (macOS / Linux).
# UNTESTED: written for macOS Terminal and common Linux terminals; adjust if your terminal differs.
#   sh machete/start_session.sh <meeting id>
KIT="$(cd "$(dirname "$0")/.." && pwd)"
PROMPT="Read machete/session-prompt.md and follow it. The meeting that just started has the id $1."
CMD="cd '$KIT' && claude --name 'Machete meeting copilot' -- \"$PROMPT\""
if [ "$(uname)" = "Darwin" ]; then
  osascript -e "tell application \"Terminal\" to do script \"$(printf '%s' "$CMD" | sed 's/\"/\\\\\"/g')\""
elif command -v gnome-terminal >/dev/null 2>&1; then
  gnome-terminal -- sh -c "$CMD; exec sh"
elif command -v x-terminal-emulator >/dev/null 2>&1; then
  x-terminal-emulator -e sh -c "$CMD; exec sh"
else
  echo "No terminal found: run this yourself:  $CMD"
fi
`````

## File: `machete/install_listener.ps1`

`````powershell
# Registers the Machete listener as a Windows scheduled task for the current user: starts one minute after you sign
# in, runs hidden, restarts if it stops. No admin rights needed.
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1            # install / update
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1 -Remove    # uninstall
# Pause it:  Disable-ScheduledTask -TaskName "Machete listener"   (Enable-ScheduledTask to resume)
param([switch]$Remove)

$name = 'Machete listener'
if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "removed"
    exit 0
}
$kit = Split-Path -Parent $PSScriptRoot
$pyw = Join-Path $kit '.venv\Scripts\pythonw.exe'
if (-not (Test-Path $pyw)) { $pyw = (Get-Command pythonw.exe -ErrorAction Stop).Source }
$action = New-ScheduledTaskAction -Execute $pyw -Argument ('"' + (Join-Path $kit 'machete\listen.py') + '"') -WorkingDirectory $kit
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$trigger.Delay = 'PT1M'
$opts = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 `
    -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $opts -Force | Out-Null
Start-ScheduledTask -TaskName $name
Write-Output "registered and started: $name"
`````
