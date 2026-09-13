#!/bin/bash
set -e

MODEL_NAME="${1:-qwen3.5:4b}"
OLLAMA_PORT=11434

echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[1;36m    Security-AI: Local AI Initializer     \033[0m"
echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[0;37m[INFO] Model: $MODEL_NAME\033[0m"
echo -e "\033[0;37m[INFO] Port: $OLLAMA_PORT\033[0m\n"

# 1. Check Ollama installation
echo -e "\033[1;33m[1/4] Checking Ollama installation...\033[0m"
if ! command -v ollama &> /dev/null; then
    echo -e "\033[1;31m[ERROR] 'ollama' command was not found.\033[0m"
    echo "Install from: https://ollama.com"
    exit 1
fi
echo -e "\033[1;32m[OK] Ollama detected on system.\033[0m"

# 2. Check if server is already running
echo -e "\033[1;33m[2/4] Checking Ollama server status...\033[0m"
if curl -s "http://localhost:$OLLAMA_PORT/api/tags" > /dev/null 2>&1; then
    echo -e "\033[1;32m[OK] Ollama server is already running.\033[0m"
else
    echo -e "\033[1;33m[INFO] Server is offline. Starting 'ollama serve' in background...\033[0m"
    ollama serve > /dev/null 2>&1 &
    
    echo -n "Waiting for API initialization..."
    until curl -s "http://localhost:$OLLAMA_PORT/api/tags" > /dev/null 2>&1; do
        sleep 1
        echo -n "."
    done
    echo ""
    echo -e "\033[1;32m[OK] Server started successfully!\033[0m"
fi

# 3. Ensure local model is available
echo -e "\033[1;33m[3/4] Checking model '$MODEL_NAME'...\033[0m"
if ! ollama list | grep -q "$MODEL_NAME"; then
    echo -e "\033[1;33m[INFO] Model '$MODEL_NAME' not found locally. Pulling model...\033[0m"
    ollama pull "$MODEL_NAME"
    echo -e "\033[1;32m[OK] Model '$MODEL_NAME' downloaded successfully!\033[0m"
else
    echo -e "\033[1;32m[OK] Model '$MODEL_NAME' is ready to use.\033[0m"
fi

# 4. Clean up legacy models
echo -e "\033[1;33m[4/4] Cleaning up legacy models...\033[0m"
if ollama list | grep -q "llama3.2"; then
    echo -e "\033[1;33m[CLEANUP] Removing deprecated model 'llama3.2:1b'...\033[0m"
    ollama rm llama3.2:1b || true
    echo -e "\033[1;32m[OK] Removed 'llama3.2:1b' successfully.\033[0m"
fi

echo ""
echo -e "\033[1;32m==========================================\033[0m"
echo -e "\033[1;32m [SUCCESS] AI engine is ready!             \033[0m"
echo -e "\033[1;32m Endpoint: http://localhost:$OLLAMA_PORT   \033[0m"
echo -e "\033[1;32m==========================================\033[0m"
