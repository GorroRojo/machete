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
