@echo off
cd /d "C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site"
echo ========================================
echo Daily SEO - %date% %time%
echo ========================================
node daily-seo-auto.js >> daily-seo.log 2>&1
echo Done at %time%
pause
