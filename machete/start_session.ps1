# Starts the Machete Claude Code session for one meeting in its own terminal window (Windows).
# Called by listen.py when a meeting starts. A previous Machete session is closed first, so each meeting starts
# with a fresh context.
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\start_session.ps1 -Meeting <meeting id>
param([string]$Meeting = '')

$kit = Split-Path -Parent $PSScriptRoot
$title = 'Machete meeting copilot'
Get-CimInstance Win32_Process -Filter "name='claude.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*$title*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) { $claude = Join-Path $env:USERPROFILE '.local\bin\claude.exe' }
$prompt = "Read machete/session-prompt.md and follow it. The meeting that just started has the id $Meeting."
$inner = Join-Path $env:TEMP 'machete-session.ps1'
@"
`$Host.UI.RawUI.WindowTitle = '$title'
Set-Location '$kit'
& '$claude' --name '$title' -- "$prompt"
"@ | Set-Content -Path $inner -Encoding utf8

$wt = Get-Command wt.exe -ErrorAction SilentlyContinue
if ($wt) {
    & wt.exe -w machete new-tab --title 'Machete' -d $kit powershell -NoProfile -NoExit -ExecutionPolicy Bypass -File $inner
} else {
    Start-Process powershell -ArgumentList '-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $inner -WorkingDirectory $kit
}
