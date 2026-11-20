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
