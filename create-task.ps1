$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site\run-seo-daily.bat'
$trigger = New-ScheduledTaskTrigger -Daily -At 09:00
$principal = New-ScheduledTaskPrincipal -UserId "Administrator" -RunLevel Highest -LogonType ServiceAccount
Register-ScheduledTask -TaskName "SuncableDailySEO" -Action $action -Trigger $trigger -Principal $principal -Description "Daily SEO automation for suncable website" -Force
Write-Host "Task created successfully"
