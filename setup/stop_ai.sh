#!/bin/bash

echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[1;36m     A encerrar a IA Local (Ollama)       \033[0m"
echo -e "\033[1;36m==========================================\033[0m"

if pgrep -f "ollama" > /dev/null; then
    echo -e "\033[1;33m[INFO] A terminar processos do Ollama...\033[0m"
    pkill -f "ollama serve" || pkill -f "ollama"
    sleep 1
    echo -e "\033[1;32m[OK] O servidor de IA foi desligado com sucesso!\033[0m"
else
    echo -e "\033[0;37m[INFO] O Ollama já se encontra desligado.\033[0m"
fi

echo -e "\033[1;36m==========================================\033[0m"
