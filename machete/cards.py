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
Kinds: answer, date, slots (find a time), task, person, fact, timezone, prep, followup, reminder, consent, list, other.
Information only (one OK button): answer, person, fact, timezone, prep, reminder, consent, list.
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
ICON = {"answer": "🔎", "date": "📅", "slots": "🗓️", "task": "✅", "person": "👤", "fact": "🔢", "timezone": "🌐", "prep": "🗂️",
        "followup": "✉️", "reminder": "⏰", "consent": "🎙️", "list": "📋", "other": "💡"}
INFO_ONLY = {"answer", "person", "fact", "timezone", "prep", "reminder", "consent", "list"}
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
        tk.Label(bar, text="Machete", bg=BG, fg=DIM, font=(FONT, 9)).pack(side="left", padx=(2, 0))
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
