"""
Script para sincronizar modelo_prediccion_meteorologica.py con modelo1_0.ipynb
Convierte el código Python en un notebook de Colab con celdas organizadas
Ejecuta: python sync_modelo_to_colab.py
"""

import json
import os
import re

def dividir_en_secciones(codigo):
    """
    Divide el código en secciones lógicas basándose en los comentarios de separación
    
    Returns:
        Lista de diccionarios con {tipo, titulo, codigo}
    """
    secciones = []
    
    # Patrones para identificar secciones
    patron_seccion = r'# ={70,}\n# (.+?)\n# ={70,}'
    
    # Dividir por secciones principales
    partes = re.split(patron_seccion, codigo)
    
    # La primera parte es el docstring y imports
    if partes[0].strip():
        secciones.append({
            'tipo': 'code',
            'titulo': 'Imports y Configuración',
            'codigo': partes[0].strip()
        })
    
    # Procesar el resto de secciones
    for i in range(1, len(partes), 2):
        if i + 1 < len(partes):
            titulo = partes[i].strip()
            codigo_seccion = partes[i + 1].strip()
            
            # Determinar si es markdown o código
            if 'PARTE' in titulo or 'CONFIGURACIÓN' in titulo:
                # Agregar como markdown
                secciones.append({
                    'tipo': 'markdown',
                    'titulo': titulo,
                    'codigo': None
                })
            
            # Agregar el código de la sección
            if codigo_seccion:
                secciones.append({
                    'tipo': 'code',
                    'titulo': titulo,
                    'codigo': codigo_seccion
                })
    
    return secciones

def crear_celda_markdown(titulo, contenido=None):
    """Crea una celda de markdown"""
    source = [f"# {titulo}\n"]
    if contenido:
        source.extend([f"{linea}\n" for linea in contenido.split('\n')])
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

def crear_celda_codigo(codigo):
    """Crea una celda de código"""
    lineas = codigo.split('\n')
    source = [f"{linea}\n" for linea in lineas]
    
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

def py_to_notebook(py_file, notebook_file):
    """
    Convierte modelo_prediccion_meteorologica.py en un notebook de Colab
    con celdas bien organizadas
    """
    
    # Leer el archivo Python
    with open(py_file, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Modificar para Colab
    codigo_colab = codigo.replace('USE_COLAB = False', 'USE_COLAB = True')
    
    # Crear estructura del notebook
    notebook = {
        "cells": [],
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
    
    # Celda 1: Badge de Colab
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {
            "id": "view-in-github",
            "colab_type": "text"
        },
        "source": [
            '<a href="https://colab.research.google.com/github/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
        ]
    })
    
    # Celda 2: Título principal
    notebook["cells"].append(crear_celda_markdown(
        "Modelo de Prediccion Meteorologica Multi-Horizonte",
        "**Predicción de variables meteorológicas en 1, 2 y 3 días**\n\n"
        "Este notebook contiene un modelo LSTM Bidireccional optimizado para predicción meteorológica.\n\n"
        "**Sincronizado automáticamente desde `modelo_prediccion_meteorologica.py`**"
    ))
    
    # Celda 3: Montar Google Drive
    notebook["cells"].append(crear_celda_markdown("Paso 1: Montar Google Drive"))
    notebook["cells"].append(crear_celda_codigo(
        "# Montar Google Drive para acceder a los datos\n"
        "from google.colab import drive\n"
        "drive.mount('/gdrive')\n\n"
        "# Verificar que los datos estén disponibles\n"
        "import os\n"
        "data_path = '/gdrive/MyDrive/Cuba_datasheet.csv'\n"
        "if os.path.exists(data_path):\n"
        "    print('✅ Datos encontrados')\n"
        "else:\n"
        "    print('Datos no encontrados. Asegurate de subir Cuba_datasheet.csv a tu Google Drive')"
    ))
    
    # Celda 4: Instalar dependencias
    notebook["cells"].append(crear_celda_markdown("Paso 2: Instalar Dependencias"))
    notebook["cells"].append(crear_celda_codigo(
        "# Instalar dependencias necesarias\n"
        "!pip install -q scikit-learn tensorflow matplotlib seaborn\n"
        "print('Dependencias instaladas')"
    ))
    
    # Dividir el código en secciones
    secciones = dividir_en_secciones(codigo_colab)
    
    # Agregar secciones al notebook
    seccion_actual = None
    codigo_acumulado = []
    
    # Agregar secciones al notebook (EXCEPTO la ejecución principal)
    seccion_actual = None
    codigo_acumulado = []
    
    for seccion in secciones:
        # Ignorar la sección de ejecución principal del script
        if 'EJECUCIÓN PRINCIPAL' in seccion['titulo']:
            continue
            
        if seccion['tipo'] == 'markdown':
            # Si hay código acumulado, agregarlo primero
            if codigo_acumulado:
                notebook["cells"].append(crear_celda_codigo('\n'.join(codigo_acumulado)))
                codigo_acumulado = []
            
            # Agregar celda de markdown
            notebook["cells"].append(crear_celda_markdown(f"## {seccion['titulo']}"))
            seccion_actual = seccion['titulo']
        
        elif seccion['tipo'] == 'code' and seccion['codigo']:
            # Acumular código
            if seccion_actual:
                codigo_acumulado.append(f"# {seccion['titulo']}\n{seccion['codigo']}")
            else:
                codigo_acumulado.append(seccion['codigo'])
    
    # Agregar código restante
    if codigo_acumulado:
        notebook["cells"].append(crear_celda_codigo('\n\n'.join(codigo_acumulado)))
    
    # ============================================================================
    # CELDAS DE EJECUCIÓN MODULAR (PASO A PASO)
    # ============================================================================
    
    notebook["cells"].append(crear_celda_markdown(
        "Paso 3: Ejecucion Modular",
        "Ejecuta las siguientes celdas paso a paso para ver el progreso detallado."
    ))
    
    # FASE 1
    notebook["cells"].append(crear_celda_markdown("### 1. Fase 1: Preparacion de Datos"))
    notebook["cells"].append(crear_celda_codigo(
        "# Cargar, limpiar y procesar datos\n"
        "preparador, datos = fase_1_preparacion_datos()"
    ))
    
    # FASE 2
    notebook["cells"].append(crear_celda_markdown("### 2. Fase 2: Entrenamiento del Modelo"))
    notebook["cells"].append(crear_celda_codigo(
        "# Entrenar modelos para todos los horizontes\n"
        "if preparador:\n"
        "    modelo = fase_2_entrenamiento(preparador, datos)"
    ))
    
    # FASE 3
    notebook["cells"].append(crear_celda_markdown("### 3. Fase 3: Testeo y Predicciones"))
    notebook["cells"].append(crear_celda_codigo(
        "# Generar predicciones con datos de prueba\n"
        "if modelo:\n"
        "    evaluador = fase_3_evaluacion_test(modelo, preparador, datos)"
    ))
    
    # FASE 4
    notebook["cells"].append(crear_celda_markdown("### 4. Fase 4: Metricas Detalladas"))
    notebook["cells"].append(crear_celda_codigo(
        "# Ver tablas de precisión (MAE, RMSE, R2)\n"
        "if evaluador:\n"
        "    fase_4_metricas_detalladas(evaluador, datos)"
    ))
    
    # FASE 5
    notebook["cells"].append(crear_celda_markdown("### 5. Fase 5: Visualizacion Grafica"))
    notebook["cells"].append(crear_celda_codigo(
        "# Configurar estilo y mostrar gráficos\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "plt.style.use('seaborn-v0_8-darkgrid')\n"
        "sns.set_palette('husl')\n\n"
        "if evaluador:\n"
        "    fase_5_visualizacion_grafica(evaluador, datos)"
    ))
    
    # FASE 6
    notebook["cells"].append(crear_celda_markdown("### 6. Fase 6: Diagnostico Automatico"))
    notebook["cells"].append(crear_celda_codigo(
        "# Generar reporte de diagnóstico y análisis de residuos\n"
        "if evaluador:\n"
        "    fase_6_diagnostico_final(evaluador, datos)"
    ))
    
    # Guardar el notebook
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"Notebook creado: {notebook_file}")
    print(f"   Desde: {py_file}")
    print(f"   Celdas: {len(notebook['cells'])}")

def main():
    """Función principal"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    py_file = os.path.join(script_dir, 'modelo_prediccion_meteorologica.py')
    notebook_file = os.path.join(script_dir, 'modelo1_0.ipynb')
    
    if not os.path.exists(py_file):
        print(f"Error: No se encontro {py_file}")
        return
    
    print("=" * 70)
    print("SINCRONIZANDO modelo_prediccion_meteorologica.py -> modelo1_0.ipynb")
    print("=" * 70)
    
    py_to_notebook(py_file, notebook_file)
    
    print("\n" + "=" * 70)
    print("SINCRONIZACION COMPLETA!")
    print("=" * 70)
    print("\nPróximos pasos:")
    print("1. Sube Cuba_datasheet.csv a tu Google Drive")
    print("2. Haz commit y push de modelo1_0.ipynb")
    print("3. Abre el notebook en Colab desde GitHub")
    print("4. ¡Ejecuta las celdas para entrenar el modelo!")

if __name__ == "__main__":
    main()
