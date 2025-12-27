@echo off
chcp 65001 >nul
cls

echo.
echo ================================================
echo   🚀 SINCRONIZACIÓN MODELO IA
echo ================================================
echo.

cd /d "d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo"

if "%~1"=="" (
    echo ❌ Error: Debes proporcionar un mensaje
    echo.
    echo Uso: sync.bat "agregue comentario"
    echo Ejemplo: sync.bat "agregué análisis de viento"
    echo.
    pause
    exit /b 1
)

echo 📝 Paso 1/3: Convirtiendo .py → .ipynb...
python sync_py_to_notebook.py

if errorlevel 1 (
    echo.
    echo ❌ Error al convertir el archivo
    pause
    exit /b 1
)

echo.
echo 📦 Paso 2/3: Preparando archivos...
git add modelo_cuba.py modelo1_0.ipynb

echo 💾 Paso 3/3: Subiendo a GitHub...
git commit -m "%~1"
git push origin base

if errorlevel 1 (
    echo.
    echo ❌ Error al sincronizar
    pause
    exit /b 1
)

echo.
echo ================================================
echo   ✅ ¡SINCRONIZACIÓN EXITOSA!
echo ================================================
echo.
echo Ahora puedes:
echo   1. Ir a: https://github.com/Danolight/Modelo_IA
echo   2. Abrir modelo1_0.ipynb
echo   3. Clic en 'Open in Colab'
echo   4. ¡Ejecutar tu código actualizado!
echo.
pause
