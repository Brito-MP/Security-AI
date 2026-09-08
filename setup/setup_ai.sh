#!/bin/bash
set -e

MODEL_NAME="${1:-llama3.2:1b}"
OLLAMA_PORT=11434

echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[1;36m  Security-AI: Inicializador Local da IA  \033[0m"
echo -e "\033[1;36m==========================================\033[0m"
echo -e "\033[0;37m[INFO] Modelo: $MODEL_NAME\033[0m"
echo -e "\033[0;37m[INFO] Porta: $OLLAMA_PORT\033[0m\n"

# 1. Verificar instalação do Ollama
echo -e "\033[1;33m[1/3] A verificar instalação do Ollama...\033[0m"
if ! command -v ollama &> /dev/null; then
    echo -e "\033[1;31m[ERRO] O comando 'ollama' não foi encontrado.\033[0m"
    echo "Instala em: https://ollama.com"
    exit 1
fi
echo -e "\033[1;32m[OK] Ollama detetado no sistema.\033[0m"

# 2. Verificar se o servidor já está a correr
echo -e "\033[1;33m[2/3] A verificar estado do servidor Ollama...\033[0m"
if curl -s "http://localhost:$OLLAMA_PORT/api/tags" > /dev/null 2>&1; then
    echo -e "\033[1;32m[OK] O servidor Ollama já está em execução.\033[0m"
else
    echo -e "\033[1;33m[INFO] Servidor desligado. A iniciar 'ollama serve' em segundo plano...\033[0m"
    ollama serve > /dev/null 2>&1 &
    
    echo -n "A aguardar inicialização da API..."
    until curl -s "http://localhost:$OLLAMA_PORT/api/tags" > /dev/null 2>&1; do
        sleep 1
        echo -n "."
    done
    echo ""
    echo -e "\033[1;32m[OK] Servidor iniciado com sucesso!\033[0m"
fi

# 3. Garantir modelo local
echo -e "\033[1;33m[3/3] A verificar modelo '$MODEL_NAME'...\033[0m"
if ! ollama list | grep -q "$MODEL_NAME"; then
    echo -e "\033[1;33m[INFO] Modelo '$MODEL_NAME' não encontrado. A transferir...\033[0m"
    ollama pull "$MODEL_NAME"
    echo -e "\033[1;32m[OK] Modelo '$MODEL_NAME' transferido com sucesso!\033[0m"
else
    echo -e "\033[1;32m[OK] Modelo '$MODEL_NAME' pronto a utilizar.\033[0m"
fi

echo ""
echo -e "\033[1;32m==========================================\033[0m"
echo -e "\033[1;32m [SUCESSO] IA pronta a receber pedidos!    \033[0m"
echo -e "\033[1;32m Endpoint: http://localhost:$OLLAMA_PORT   \033[0m"
echo -e "\033[1;32m==========================================\033[0m"
