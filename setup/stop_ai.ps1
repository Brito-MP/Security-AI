Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     Shutting down Local AI (Ollama)      " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$procs = Get-Process "ollama*" -ErrorAction SilentlyContinue

if ($procs) {
    Write-Host "[INFO] Terminating Ollama processes..." -ForegroundColor Yellow
    Stop-Process -Name "ollama*" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    
    $remaining = Get-Process "ollama*" -ErrorAction SilentlyContinue
    if (-not $remaining) {
        Write-Host "[OK] AI server terminated successfully!" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Some processes are still active. Retrying..." -ForegroundColor Yellow
        $remaining | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Shutdown completed." -ForegroundColor Green
    }
} else {
    Write-Host "[INFO] Ollama is already stopped." -ForegroundColor Gray
}

Write-Host "==========================================" -ForegroundColor Cyan
