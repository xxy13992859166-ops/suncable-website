$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("C:\Users\Administrator\Desktop\Suncable SEO Daily.lnk")
$sc.TargetPath = "cmd.exe"
$sc.Arguments = "/c cd /d C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site && node daily-seo-auto.js >> daily-seo.log 2>&1"
$sc.WorkingDirectory = "C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site"
$sc.Description = "Daily SEO automation for suncable website"
$sc.Save()
Write-Host "Desktop shortcut created: Suncable SEO Daily.lnk"
