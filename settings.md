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
