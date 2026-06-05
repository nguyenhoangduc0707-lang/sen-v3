@echo off
chcp 65001 > nul
echo ========================================
echo   GEMINI 3.5 FLASH - GOOGLE GENAI TEST
echo ========================================
echo.

REM Set your API key here (thay YOUR_API_KEY b?ng key th?t)
set GOOGLE_API_KEY=gemini-3.5-flash
set GOOGLE_GENAI_USE_ENTERPRISE=False

echo Running test with Gemini 3.5 Flash...
echo.
python test_simple.py

echo.
echo ========================================
echo Test completed!
echo ========================================
pause
