#!/bin/bash

echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[1;36m     Shutting down Local AI (Ollama)      \033[0m"
echo -e "\033[1;36m==========================================\033[0m"

if pgrep -f "ollama" > /dev/null; then
    echo -e "\033[1;33m[INFO] Terminating Ollama processes...\033[0m"
    pkill -f "ollama serve" || pkill -f "ollama"
    sleep 1
    echo -e "\033[1;32m[OK] AI server stopped successfully!\033[0m"
else
    echo -e "\033[0;37m[INFO] Ollama is already stopped.\033[0m"
fi

echo -e "\033[1;36m==========================================\033[0m"
