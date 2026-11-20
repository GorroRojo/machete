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
