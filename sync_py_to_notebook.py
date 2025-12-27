"""
Script para sincronizar modelo_cuba.py con modelo1_0.ipynb automáticamente
Ejecuta este script cada vez que modifiques modelo_cuba.py
"""

import json
import os

def py_to_notebook(py_file, notebook_file):
    """
    Convierte un archivo .py en un notebook .ipynb
    Mantiene el formato de Colab
    """
    
    # Leer el archivo Python
    with open(py_file, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Crear estructura del notebook
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {
                    "id": "view-in-github",
                    "colab_type": "text"
                },
                "source": [
                    '<a href="https://colab.research.google.com/github/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 🌤️ Modelo de Análisis Meteorológico de Cuba\n",
                    "\n",
                    "**Sincronizado automáticamente desde `modelo_cuba.py`**\n",
                    "\n",
                    "Este notebook se actualiza automáticamente cuando modificas el archivo Python local."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📦 Configuración inicial"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Montar Google Drive\n",
                    "from google.colab import drive\n",
                    "drive.mount('/gdrive')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🚀 Código Principal\n",
                    "\n",
                    "El siguiente código fue generado automáticamente desde `modelo_cuba.py`"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": []
            }
        ],
        "metadata": {
            "colab": {
                "provenance": [],
                "authorship_tag": "ABX9TyMxxx",
                "include_colab_link": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    # Modificar el código para que funcione en Colab
    codigo_colab = codigo.replace('USE_COLAB = False', 'USE_COLAB = True')
    
    # Dividir el código en líneas para el notebook
    lineas_codigo = codigo_colab.split('\n')
    
    # Agregar el código a la última celda
    notebook["cells"][-1]["source"] = lineas_codigo
    
    # Guardar el notebook
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Notebook actualizado: {notebook_file}")
    print(f"   Desde: {py_file}")
    print(f"   Líneas de código: {len(lineas_codigo)}")


def main():
    """Función principal"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    py_file = os.path.join(script_dir, 'modelo_cuba.py')
    notebook_file = os.path.join(script_dir, 'modelo1_0.ipynb')
    
    if not os.path.exists(py_file):
        print(f"❌ Error: No se encontró {py_file}")
        return
    
    print("=" * 60)
    print("🔄 SINCRONIZANDO .py → .ipynb")
    print("=" * 60)
    
    py_to_notebook(py_file, notebook_file)
    
    print("\n" + "=" * 60)
    print("✅ ¡SINCRONIZACIÓN COMPLETA!")
    print("=" * 60)
    print("\nAhora puedes:")
    print("1. Hacer commit y push de modelo1_0.ipynb")
    print("2. Abrir el notebook en Colab desde GitHub")
    print("3. ¡Ejecutar tu código actualizado!")


if __name__ == "__main__":
    main()
