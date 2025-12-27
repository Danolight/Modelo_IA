"""
Script para subir cambios a GitHub automáticamente
Ejecuta: python upload_github.py "Mensaje del commit"
"""

import os
import sys
import subprocess

def run_command(command):
    """Ejecuta un comando de shell y muestra la salida"""
    print(f"🚀 Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar: {command}")
        print(e.stderr)
        return False

def main():
    """Función principal"""
    # Obtener mensaje del commit
    if len(sys.argv) > 1:
        commit_message = sys.argv[1]
    else:
        commit_message = "Actualización automática del modelo meteorológico"
    
    print("="*60)
    print("octocat: SUBIENDO CAMBIOS A GITHUB")
    print("="*60)
    
    # 1. Verificar estado
    print("\n📊 Estado actual:")
    run_command("git status")
    
    # 2. Agregar archivos
    print("\n➕ Agregando archivos...")
    if not run_command("git add ."):
        return
    
    # 3. Commit
    print(f"\n📝 Creando commit: '{commit_message}'")
    if not run_command(f'git commit -m "{commit_message}"'):
        print("⚠️  No hay cambios para commitear")
    
    # 4. Push
    print("\n⬆️  Subiendo a GitHub...")
    if run_command("git push"):
        print("\n" + "="*60)
        print("✅ ¡CAMBIOS SUBIDOS EXITOSAMENTE!")
        print("="*60)
    else:
        print("\n❌ Error al subir cambios. Verifica tu conexión o credenciales.")

if __name__ == "__main__":
    main()
