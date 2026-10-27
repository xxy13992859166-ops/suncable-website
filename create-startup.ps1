$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Suncable SEO Daily.lnk")
$sc.TargetPath = "C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site\daily-seo.bat"
$sc.WorkingDirectory = "C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site"
$sc.Description = "Daily SEO automation for suncable website"
$sc.Save()
Write-Host "Startup shortcut created successfully"
