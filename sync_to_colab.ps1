# ============================================================================
# SCRIPT DE SINCRONIZACIÓN A COLAB
# ============================================================================
# Este script sube tus cambios locales a GitHub para que Colab los vea
#
# Uso: .\sync_to_colab.ps1 "mensaje del commit"
# Ejemplo: .\sync_to_colab.ps1 "Agregué análisis de viento"

param(
    [string]$mensaje = "Actualización desde local"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  SINCRONIZANDO CAMBIOS A COLAB" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: No estás en un repositorio Git" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde: modelo_ia_repo\" -ForegroundColor Yellow
    exit 1
}

Write-Host "📝 Agregando archivos..." -ForegroundColor Yellow
git add .

Write-Host "💾 Creando commit: '$mensaje'" -ForegroundColor Yellow
git commit -m "$mensaje"

Write-Host "🚀 Subiendo a GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡Sincronización exitosa!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ahora en Colab ejecuta:" -ForegroundColor Cyan
    Write-Host "  !git pull origin main" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Error al sincronizar" -ForegroundColor Red
    Write-Host "   Verifica tu conexión y credenciales de Git" -ForegroundColor Yellow
    Write-Host ""
}
