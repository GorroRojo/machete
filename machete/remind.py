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
