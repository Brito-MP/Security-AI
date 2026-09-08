@echo off
echo ==========================================
echo      A encerrar a IA Local (Ollama)     
echo ==========================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0stop_ai.ps1"

echo.
timeout /t 3 >nul
