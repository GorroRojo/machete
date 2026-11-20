"""Builds SETUP-PROMPT.md: the instructions below plus every kit file inline, so it works with no download.
Run after changing any kit file:  python build_setup_prompt.py
"""
import pathlib

KIT = pathlib.Path(__file__).resolve().parent
FILES = ["settings.md", "README.md", "requirements.txt", ".gitignore", ".claude/settings.json",
         "machete/common.py", "machete/listen.py", "machete/cards.py", "machete/follow.py", "machete/remind.py",
         "machete/fake_meeting.py", "machete/session-prompt.md", "machete/start_session.ps1",
         "machete/start_session.sh", "machete/install_listener.ps1"]

HEAD = """# Set up Machete, a live meeting copilot (paste all of this into Claude Code)

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
   - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File machete\\install_listener.ps1`.
   - macOS (untested, say so): a LaunchAgent plist in `~/Library/LaunchAgents/` running the venv's python with
     `machete/listen.py`, WorkingDirectory the kit folder, RunAtLoad and KeepAlive true; `launchctl load` it.
   - Audio option: also tell me that each meeting starts with `python machete/listen.py audio`.
7. Show me a first card: `machete/cards.py add date "Thu · 15:00\\nQ3 review with Sam\\nTest card: tap ✓" --source
   "Machete setup"`, then open the window in the background (`machete/cards.py window`, with pythonw on Windows).
   Ask me to tap ✓, confirm the tap appeared in `data/live.log`, then `machete/cards.py done <id> "Setup works"`.
8. Finish with five lines: which card actions will work with my connectors, how to pause (`Copilot: off` in
   settings.md), how to uninstall (`install_listener.ps1 -Remove` and delete the folder), that private meetings are
   skipped by the keywords in settings.md, and to tell people when I'm recording.

"""


def main() -> None:
    parts = [HEAD]
    for rel in FILES:
        text = (KIT / rel).read_text(encoding="utf-8").rstrip("\n")
        lang = {"py": "python", "ps1": "powershell", "sh": "sh", "json": "json", "md": "markdown"}.get(
            rel.rsplit(".", 1)[-1], "text")
        parts.append(f"## File: `{rel}`\n\n`````{lang}\n{text}\n`````\n")
    out = "\n".join(parts)
    (KIT / "SETUP-PROMPT.md").write_text(out, encoding="utf-8")
    print(f"SETUP-PROMPT.md: {len(out):,} characters")


if __name__ == "__main__":
    main()
