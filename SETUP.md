# Set up Machete (instructions for Claude Code)

You are setting up **Machete** on this computer for the user. Machete follows the user's meetings live and offers rare
one-tap cards: answers to questions asked in the meeting, heads-ups about what's being discussed, dates, find-a-time,
tasks, people, time zones, a prep card at the start and a follow-up draft at the end. Nothing acts without their ✓.
You are working inside the cloned `machete` folder; every file the kit needs is already here.

1. **Ask the user these five questions in one short message** (offer the choices; one line each):
   1. Recorder: **Wispr Flow** / **a tool that writes a live transcript file** (which file or folder?) /
      **my mic and computer sound, transcribed on this PC**.
   2. Calendar: which one do they use? Check which Claude connectors you have (calendar, email, Slack, tasks, CRM,
      sheets, Drive) and tell them what you found.
   3. Task tool (ClickUp, Asana, Notion, Linear, other, or none = local reminders on this computer).
   4. Where their notes and documents live (a folder on this computer, Notion, Drive, a CRM, or nowhere), and whether
      web lookups for public facts should be on (default on).
   5. Card language (or "the meeting's language").
2. Fill in `settings.md` from the answers (Transcript source: `wispr`, `file` with the Transcript file path, or
   `audio`; their tools; where to look things up; web lookups; language). If a calendar connector shows their name and
   time zone, fill those in too. Change nothing else in the kit.
3. Check Python 3.11+ with tkinter (`python -c "import tkinter"`). If it's missing, tell them how to install it and
   stop. Create a venv inside the folder: `python -m venv .venv`.
4. Only for the audio option: `.venv` python `-m pip install -r requirements.txt`.
5. Run the fake-meeting test with the venv python: `machete/fake_meeting.py --check`. It must print PASS; if not, fix
   the cause and run it again.
6. Register the background listener (ask first; it starts at sign-in and runs hidden):
   - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1`.
   - macOS (untested, say so): a LaunchAgent plist in `~/Library/LaunchAgents/` running the venv's python with
     `machete/listen.py`, WorkingDirectory this folder, RunAtLoad and KeepAlive true; `launchctl load` it.
   - Audio option: also tell them that each meeting starts with `python machete/listen.py audio`.
7. Show a first card: `machete/cards.py add answer "Quoted: $48,000\nProposal v2, sent 3 Feb\nTest card: tap OK"
   --source "Machete setup" --link "Example source|https://example.com"`, then open the window in the background
   (`machete/cards.py window`, with pythonw on Windows). Ask them to tap it, confirm the tap appeared in
   `data/live.log`, then `machete/cards.py done <id> "Setup works"`.
8. Finish with five lines: which card actions will work with their connectors, how to pause (`Copilot: off` in
   settings.md), how to uninstall (`install_listener.ps1 -Remove` and delete the folder), that private meetings are
   skipped by the keywords in settings.md, and to tell people when they're recording.

To update later: `git pull` in this folder (settings.md is theirs; keep their copy if git reports a conflict).
