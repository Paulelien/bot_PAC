# Script PowerShell para mantener la API del Chatbot PAC activa
# Consulta la API cada minuto para evitar el "cold start"

param(
    [string]$ApiUrl = "http://localhost:5001/api/health",
    [int]$IntervalMinutes = 1
)

Write-Host "🚀 Iniciando keep-alive para API del Chatbot PAC" -ForegroundColor Green
Write-Host "📡 URL: $ApiUrl" -ForegroundColor Cyan
Write-Host "⏰ Intervalo: $IntervalMinutes minuto(s)" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Gray

function Test-ApiHealth {
    try {
        $response = Invoke-RestMethod -Uri $ApiUrl -Method Get -TimeoutSec 10
        $timestamp = Get-Date -Format "HH:mm:ss"
        Write-Host "✅ [$timestamp] API activa - Status: 200" -ForegroundColor Green
    }
    catch {
        $timestamp = Get-Date -Format "HH:mm:ss"
        Write-Host "❌ [$timestamp] Error conectando a la API: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Ejecutar inmediatamente la primera vez
Test-ApiHealth

# Bucle principal
try {
    while ($true) {
        Start-Sleep -Seconds ($IntervalMinutes * 60)
        Test-ApiHealth
    }
}
catch {
    Write-Host "`n🛑 Deteniendo keep-alive..." -ForegroundColor Yellow
    Write-Host "✅ Script terminado" -ForegroundColor Green
}

