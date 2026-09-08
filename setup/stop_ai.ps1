Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     A encerrar a IA Local (Ollama)       " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$procs = Get-Process "ollama*" -ErrorAction SilentlyContinue

if ($procs) {
    Write-Host "[INFO] A terminar processos do Ollama..." -ForegroundColor Yellow
    Stop-Process -Name "ollama*" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    
    # Confirmar encerramento
    $remaining = Get-Process "ollama*" -ErrorAction SilentlyContinue
    if (-not $remaining) {
        Write-Host "[OK] O servidor de IA foi encerrado com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Alguns processos ainda estao ativos. A tentar novamente..." -ForegroundColor Yellow
        $remaining | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Encerramento concluido." -ForegroundColor Green
    }
} else {
    Write-Host "[INFO] O Ollama ja se encontra desligado." -ForegroundColor Gray
}

Write-Host "==========================================" -ForegroundColor Cyan
