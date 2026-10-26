@echo off
chcp 65001 >nul
cd /d "C:\Users\Administrator\Documents\Codex\2026-10-13\n-h-5\outputs\suncable-site"
echo ========================================
echo Suncable Daily SEO Automation
echo Date: %date% Time: %time%
echo ========================================
echo.
node daily-seo-auto.js
echo.
echo ========================================
echo Done!
echo ========================================
