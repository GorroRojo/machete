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
