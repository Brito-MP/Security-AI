param(
    [int]$Port = 11434
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     Verificacao do Estado do Ollama      " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verificar processos do Windows
$proc = Get-Process "ollama*" -ErrorAction SilentlyContinue
if ($proc) {
    $pids = ($proc | Select-Object -ExpandProperty Id) -join ", "
    Write-Host "[PROCESSO] Ollama em execucao no Windows (PID: $pids)." -ForegroundColor Green
} else {
    Write-Host "[PROCESSO] Nenhum processo 'ollama' detetado." -ForegroundColor Red
}

# 2. Verificar resposta da API
$apiOnline = $false
try {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
    $apiOnline = $true
    Write-Host "[API]      Servidor ativo em http://127.0.0.1:$Port" -ForegroundColor Green
    $models = $res.models | ForEach-Object { $_.name }
    if ($models) {
        Write-Host "[MODELOS]  Disponiveis: $($models -join ', ')" -ForegroundColor Yellow
    } else {
        Write-Host "[MODELOS]  Nenhum modelo descarregado." -ForegroundColor DarkYellow
    }
} catch {
    Write-Host "[API]      Inativa (servidor desligado)." -ForegroundColor Gray
}

# 3. Modelos em memoria (GPU/RAM)
if ($apiOnline) {
    Write-Host ""
    Write-Host "[MEMORIA / GPU] Modelos carregados:" -ForegroundColor Gray
    ollama ps
}
Write-Host "==========================================" -ForegroundColor Cyan
