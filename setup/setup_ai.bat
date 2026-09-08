@echo off
setlocal enabledelayedexpansion

set MODEL_NAME=llama3.2:1b
set OLLAMA_PORT=11434

echo ==========================================
echo   Security-AI: Inicializador Local da IA  
echo ==========================================
echo [INFO] Modelo: %MODEL_NAME%
echo [INFO] Porta: %OLLAMA_PORT%
echo.

:: 1. Verificar instalação do Ollama
echo [1/3] A verificar instalacao do Ollama...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] O comando 'ollama' nao foi encontrado.
    echo Instala atraves do site oficial: https://ollama.com
    exit /b 1
)
echo [OK] Ollama detetado no sistema.

:: 2. Verificar se o servidor já está ativo na porta designada
echo [2/3] A verificar estado do servidor Ollama...
netstat -o -n -a | findstr ":%OLLAMA_PORT%" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] O servidor Ollama ja esta em execucao.
) else (
    echo [INFO] A iniciar 'ollama serve' em segundo plano...
    start "" /b ollama serve >nul 2>&1
    timeout /t 3 >nul
    echo [OK] Servidor iniciado com sucesso.
)

:: 3. Garantir o modelo local
echo [3/3] A verificar modelo '%MODEL_NAME%'...
ollama list | findstr /C:"%MODEL_NAME%" >nul
if %errorlevel% neq 0 (
    echo [INFO] Modelo '%MODEL_NAME%' nao encontrado. A transferir...
    ollama pull %MODEL_NAME%
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao transferir modelo '%MODEL_NAME%'.
        exit /b 1
    )
    echo [OK] Transferencia concluida!
) else (
    echo [OK] Modelo '%MODEL_NAME%' pronto a utilizar.
)

echo.
echo ==========================================
echo  [SUCESSO] IA pronta a receber pedidos!
echo  Endpoint: http://localhost:%OLLAMA_PORT%
echo ==========================================
