@echo off
echo ==========================================
echo      Verificacao do Estado do Ollama     
echo ==========================================
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0check_status.ps1"
echo.
pause
