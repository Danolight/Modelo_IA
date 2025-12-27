# ============================================================================
# SCRIPT DE SINCRONIZACIÓN DESDE COLAB
# ============================================================================
# Este script descarga los cambios que hiciste en Colab a tu PC local
#
# Uso: .\sync_from_colab.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DESCARGANDO CAMBIOS DESDE COLAB" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: No estás en un repositorio Git" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde: modelo_ia_repo\" -ForegroundColor Yellow
    exit 1
}

Write-Host "📥 Descargando cambios desde GitHub..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡Sincronización exitosa!" -ForegroundColor Green
    Write-Host "   Tus archivos locales están actualizados" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Error al sincronizar" -ForegroundColor Red
    Write-Host "   Puede que tengas conflictos. Revisa los archivos." -ForegroundColor Yellow
    Write-Host ""
}
