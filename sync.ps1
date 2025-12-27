# ============================================================================
# SCRIPT DE SINCRONIZACIÓN AUTOMÁTICA
# ============================================================================
# Este script:
# 1. Convierte modelo_cuba.py → modelo1_0.ipynb
# 2. Sube los cambios a GitHub
# 3. Listo para abrir en Colab
#
# Uso: .\sync.ps1 "mensaje del commit"
# Ejemplo: .\sync.ps1 "Agregué análisis de viento"

param(
    [string]$mensaje = "Actualización automática"
)

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  🔄 SINCRONIZACIÓN AUTOMÁTICA" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Convertir .py a .ipynb
Write-Host "📝 Paso 1/3: Convirtiendo .py → .ipynb..." -ForegroundColor Yellow
python sync_py_to_notebook.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Error al convertir el archivo" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Paso 2: Agregar archivos a Git
Write-Host "📦 Paso 2/3: Preparando archivos..." -ForegroundColor Yellow
git add modelo_cuba.py modelo1_0.ipynb

# Paso 3: Commit y Push
Write-Host "💾 Paso 3/3: Subiendo a GitHub..." -ForegroundColor Yellow
git commit -m "$mensaje"
git push origin base

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  ✅ ¡SINCRONIZACIÓN EXITOSA!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ahora puedes:" -ForegroundColor Cyan
    Write-Host "  1. Ir a: https://github.com/Danolight/Modelo_IA" -ForegroundColor White
    Write-Host "  2. Abrir modelo1_0.ipynb" -ForegroundColor White
    Write-Host "  3. Clic en 'Open in Colab'" -ForegroundColor White
    Write-Host "  4. ¡Ejecutar tu código actualizado!" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "❌ Error al sincronizar" -ForegroundColor Red
    Write-Host "   Verifica tu conexión y credenciales de Git" -ForegroundColor Yellow
    Write-Host ""
}
