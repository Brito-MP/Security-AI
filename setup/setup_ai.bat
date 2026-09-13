@echo off
setlocal enabledelayedexpansion

set MODEL_NAME=qwen3.5:4b
set OLLAMA_PORT=11434

echo ==========================================
echo    Security-AI: Local AI Initializer     
echo ==========================================
echo [INFO] Model: %MODEL_NAME%
echo [INFO] Port: %OLLAMA_PORT%
echo.

:: 1. Verify Ollama installation
echo [1/4] Checking Ollama installation...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'ollama' command was not found.
    echo Install from official website: https://ollama.com
    exit /b 1
)
echo [OK] Ollama detected on system.

:: 2. Check if server is running
echo [2/4] Checking Ollama server status...
netstat -o -n -a | findstr ":%OLLAMA_PORT%" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] Ollama server is already running.
) else (
    echo [INFO] Starting 'ollama serve' in background...
    start "" /b ollama serve >nul 2>&1
    timeout /t 3 >nul
    echo [OK] Server started successfully.
)

:: 3. Ensure local model is available
echo [3/4] Checking model '%MODEL_NAME%'...
ollama list | findstr /C:"%MODEL_NAME%" >nul
if %errorlevel% neq 0 (
    echo [INFO] Model '%MODEL_NAME%' not found locally. Pulling model...
    ollama pull %MODEL_NAME%
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to pull model '%MODEL_NAME%'.
        exit /b 1
    )
    echo [OK] Download complete!
) else (
    echo [OK] Model '%MODEL_NAME%' is ready to use.
)

:: 4. Clean up legacy models
echo [4/4] Cleaning up legacy models...
ollama list | findstr /C:"llama3.2" >nul
if %errorlevel% equ 0 (
    echo [CLEANUP] Removing deprecated model 'llama3.2:1b'...
    ollama rm llama3.2:1b >nul 2>&1
    echo [OK] Removed 'llama3.2:1b' successfully.
)

echo.
echo ==========================================
echo  [SUCCESS] AI engine is ready!
echo  Endpoint: http://localhost:%OLLAMA_PORT%
echo ==========================================
