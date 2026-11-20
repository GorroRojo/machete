# Registers the Machete listener as a Windows scheduled task for the current user: starts one minute after you sign
# in, runs hidden, restarts if it stops. No admin rights needed.
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1            # install / update
#   powershell -NoProfile -ExecutionPolicy Bypass -File machete\install_listener.ps1 -Remove    # uninstall
# Pause it:  Disable-ScheduledTask -TaskName "Machete listener"   (Enable-ScheduledTask to resume)
param([switch]$Remove)

$name = 'Machete listener'
if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "removed"
    exit 0
}
$kit = Split-Path -Parent $PSScriptRoot
$pyw = Join-Path $kit '.venv\Scripts\pythonw.exe'
if (-not (Test-Path $pyw)) { $pyw = (Get-Command pythonw.exe -ErrorAction Stop).Source }
$action = New-ScheduledTaskAction -Execute $pyw -Argument ('"' + (Join-Path $kit 'machete\listen.py') + '"') -WorkingDirectory $kit
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$trigger.Delay = 'PT1M'
$opts = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 `
    -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $opts -Force | Out-Null
Start-ScheduledTask -TaskName $name
Write-Output "registered and started: $name"
