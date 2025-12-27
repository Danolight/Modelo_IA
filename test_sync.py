"""
PRUEBA RÁPIDA DEL FLUJO DE TRABAJO
===================================

Este archivo es solo para probar que la sincronización funciona.
Puedes editarlo, guardarlo, y ver los cambios en Colab.

INSTRUCCIONES:
1. Modifica este archivo (agrega tu nombre abajo)
2. Guarda el archivo (Ctrl+S)
3. Ejecuta: .\sync_to_colab.ps1 "prueba de sincronización"
4. Ve a Colab y ejecuta: !git pull origin base
5. Ejecuta: %run test_sync.py
6. ¡Deberías ver tu nombre impreso!
"""

# ============================================================================
# EDITA AQUÍ
# ============================================================================

TU_NOMBRE = "Tu nombre aquí"  # <-- Cambia esto por tu nombre
FECHA_PRUEBA = "2025-12-27"

# ============================================================================
# NO EDITES ABAJO DE ESTA LÍNEA
# ============================================================================

def test_sincronizacion():
    """Prueba que la sincronización funciona correctamente"""
    print("=" * 60)
    print("🎉 ¡SINCRONIZACIÓN EXITOSA!")
    print("=" * 60)
    print(f"\n👤 Usuario: {TU_NOMBRE}")
    print(f"📅 Fecha de prueba: {FECHA_PRUEBA}")
    print(f"\n✅ El archivo fue modificado en local y ejecutado en Colab")
    print("\n" + "=" * 60)
    
    # Verificar que estamos en Colab o local
    try:
        import google.colab
        print("🌐 Ejecutando en: Google Colab")
    except:
        print("💻 Ejecutando en: Local (tu PC)")
    
    print("=" * 60)

if __name__ == "__main__":
    test_sincronizacion()
