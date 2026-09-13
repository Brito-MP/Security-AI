param(
    [string]$Model = "qwen3.5:4b",
    [int]$Port = 11434
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "    Security-AI: Local AI Initializer     " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "[INFO] Selected Model: $Model" -ForegroundColor Gray
Write-Host "[INFO] API Port: $Port" -ForegroundColor Gray
Write-Host ""

# 1. Verify Ollama installation
Write-Host "[1/4] Checking Ollama installation..." -ForegroundColor Yellow
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] 'ollama' command was not found on this system." -ForegroundColor Red
    Write-Host "Please install Ollama from official website: https://ollama.com" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Ollama detected on system." -ForegroundColor Green

# 2. Verify if server is already running on designated port
Write-Host "[2/4] Checking Ollama server status on port $Port..." -ForegroundColor Yellow
$serverReady = $false
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
    $serverReady = $true
} catch {
    $serverReady = $false
}

if ($serverReady) {
    Write-Host "[OK] Ollama server is already running." -ForegroundColor Green
} else {
    Write-Host "[INFO] Server is offline. Starting 'ollama serve' in background..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden

    Write-Host -NoNewline "Waiting for API initialization..." -ForegroundColor Gray
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
        Write-Host "[ERROR] Timeout while waiting for Ollama server startup." -ForegroundColor Red
        Write-Host "Try starting manually in a separate terminal: ollama serve" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Ollama server started successfully!" -ForegroundColor Green
}

# 3. Ensure local model is downloaded
Write-Host "[3/4] Checking model '$Model'..." -ForegroundColor Yellow
$installedModels = ollama list
$modelFound = $false

foreach ($line in $installedModels) {
    if ($line -match "^$Model\s") {
        $modelFound = $true
        break
    }
}

if ($modelFound) {
    Write-Host "[OK] Model '$Model' is already downloaded and ready." -ForegroundColor Green
} else {
    Write-Host "[INFO] Model '$Model' not found locally. Pulling model..." -ForegroundColor Yellow
    ollama pull $Model
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to pull model '$Model'." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "[OK] Model '$Model' downloaded successfully!" -ForegroundColor Green
}

# 4. Clean up legacy models (e.g. llama3.2:1b)
Write-Host "[4/4] Cleaning up legacy models..." -ForegroundColor Yellow
$legacyModels = @("llama3.2:1b", "llama3.2")
$currentList = ollama list
foreach ($legacy in $legacyModels) {
    if ($currentList -match "^$legacy\s") {
        Write-Host "[CLEANUP] Removing deprecated model '$legacy'..." -ForegroundColor Yellow
        ollama rm $legacy | Out-Null
        Write-Host "[OK] Removed '$legacy' successfully." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " [SUCCESS] AI engine is ready for prompts! " -ForegroundColor Green
Write-Host " Endpoint: http://127.0.0.1:$Port        " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
