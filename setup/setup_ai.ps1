param(
    [string]$Model = "llama3.2:1b",
    [int]$Port = 11434
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Security-AI: Inicializador Local da IA  " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "[INFO] Modelo selecionado: $Model" -ForegroundColor Gray
Write-Host "[INFO] Porta da API: $Port" -ForegroundColor Gray
Write-Host ""

# 1. Verificar se o Ollama está instalado
Write-Host "[1/3] A verificar instalação do Ollama..." -ForegroundColor Yellow
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] O comando 'ollama' não foi encontrado no sistema." -ForegroundColor Red
    Write-Host "Por favor, instala o Ollama através do site oficial: https://ollama.com" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Ollama detetado no sistema." -ForegroundColor Green

# 2. Verificar se o servidor já está ativo na porta designada
Write-Host "[2/3] A verificar estado do servidor Ollama na porta $Port..." -ForegroundColor Yellow
$serverReady = $false
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
    $serverReady = $true
} catch {
    $serverReady = $false
}

if ($serverReady) {
    Write-Host "[OK] O servidor Ollama já está em execução." -ForegroundColor Green
} else {
    Write-Host "[INFO] Servidor desligado. A iniciar 'ollama serve' em segundo plano..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden

    Write-Host -NoNewline "A aguardar inicialização da API..." -ForegroundColor Gray
    $retries = 15
    while (-not $serverReady -and $retries -gt 0) {
        Start-Sleep -Seconds 1
        Write-Host -NoNewline "." -ForegroundColor Gray
        try {
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
            $serverReady = $true
        } catch {
            $retries--
        }
    }
    Write-Host ""

    if (-not $serverReady) {
        Write-Host "[ERRO] Tempo limite esgotado ao aguardar o arranque do Ollama." -ForegroundColor Red
        Write-Host "Tenta executar manualmente num terminal: ollama serve" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Servidor Ollama iniciado com sucesso!" -ForegroundColor Green
}

# 3. Garantir que o modelo local está descarregado
Write-Host "[3/3] A verificar modelo '$Model'..." -ForegroundColor Yellow
$installedModels = ollama list
$modelFound = $false

foreach ($line in $installedModels) {
    if ($line -match "^$Model\s") {
        $modelFound = $true
        break
    }
}

if ($modelFound) {
    Write-Host "[OK] Modelo '$Model' já se encontra descarregado e pronto." -ForegroundColor Green
} else {
    Write-Host "[INFO] Modelo '$Model' não encontrado localmente. A transferir..." -ForegroundColor Yellow
    ollama pull $Model
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao descarregar o modelo '$Model'." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "[OK] Modelo '$Model' descarregado com sucesso!" -ForegroundColor Green
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " [SUCESSO] IA pronta a receber pedidos!    " -ForegroundColor Green
Write-Host " Endpoint: http://127.0.0.1:$Port        " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
