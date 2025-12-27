# ============================================================================
# INICIO RÁPIDO - Ejecuta este script desde cualquier lugar
# ============================================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  🚀 MODELO IA - INICIO RÁPIDO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Detectar directorio actual
$currentDir = Get-Location
$targetDir = "d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo"

Write-Host "📍 Directorio actual: $currentDir" -ForegroundColor Yellow

# Verificar si estamos en el directorio correcto
if ($currentDir.Path -eq $targetDir) {
    Write-Host "✅ Ya estás en el directorio correcto" -ForegroundColor Green
}
else {
    Write-Host "🔄 Cambiando al directorio correcto..." -ForegroundColor Yellow
    Set-Location $targetDir
    Write-Host "✅ Directorio cambiado a: $targetDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  📝 COMANDOS DISPONIBLES" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para sincronizar tus cambios:" -ForegroundColor White
Write-Host "  .\sync.ps1 `"descripción de cambios`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ejemplo:" -ForegroundColor White
Write-Host "  .\sync.ps1 `"agregué análisis de viento`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
