param(
    [int]$Port = 11434
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "         Ollama Service Status            " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check OS processes
$proc = Get-Process "ollama*" -ErrorAction SilentlyContinue
if ($proc) {
    $pids = ($proc | Select-Object -ExpandProperty Id) -join ", "
    Write-Host "[PROCESS] Ollama is running (PID: $pids)." -ForegroundColor Green
} else {
    Write-Host "[PROCESS] No active 'ollama' processes detected." -ForegroundColor Red
}

# 2. Check API response
$apiOnline = $false
try {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
    $apiOnline = $true
    Write-Host "[API]     Server is active at http://127.0.0.1:$Port" -ForegroundColor Green
    $models = $res.models | ForEach-Object { $_.name }
    if ($models) {
        Write-Host "[MODELS]  Available: $($models -join ', ')" -ForegroundColor Yellow
    } else {
        Write-Host "[MODELS]  No models downloaded yet." -ForegroundColor DarkYellow
    }
} catch {
    Write-Host "[API]     Inactive (server offline)." -ForegroundColor Gray
}

# 3. Models in memory (VRAM/RAM)
if ($apiOnline) {
    Write-Host ""
    Write-Host "[MEMORY / GPU] Loaded models in memory:" -ForegroundColor Gray
    ollama ps
}
Write-Host "==========================================" -ForegroundColor Cyan
