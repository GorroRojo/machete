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
