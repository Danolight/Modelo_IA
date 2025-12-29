import nbformat as nbf
import os

def py_to_notebook(py_file, ipynb_file):
    nb = nbf.v4.new_notebook()
    
    with open(py_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Celda de instalación/setup para Colab
    setup_code = """# @title Configuración e Instalación
import os

# Clonar repositorio si no existe
if not os.path.exists('modelo_ia_repo'):
    !git clone https://github.com/Danolight/Modelo_IA.git
    %cd modelo_ia_repo
else:
    %cd modelo_ia_repo
    !git pull

# Montar Google Drive
from google.colab import drive
if not os.path.exists('/gdrive'):
    drive.mount('/gdrive')

# Instalar dependencias
!pip install -r requirements.txt
"""
    
    nb.cells.append(nbf.v4.new_code_cell(setup_code))
    
    # Celda con el código del script
    nb.cells.append(nbf.v4.new_code_cell(code))
    
    # Celda para ejecutar
    run_code = """# @title Ejecutar Evaluación
import importlib
import sys

# Forzar recarga del módulo para asegurar que se usa la última versión tras un git pull
if 'modelo_prediccion_meteorologica' in sys.modules:
    import modelo_prediccion_meteorologica
    importlib.reload(modelo_prediccion_meteorologica)
    print("Módulo modelo_prediccion_meteorologica recargado exitosamente.")

if __name__ == "__main__":
    main()
"""
    nb.cells.append(nbf.v4.new_code_cell(run_code))

    with open(ipynb_file, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"Notebook creado: {ipynb_file}")

if __name__ == "__main__":
    py_to_notebook('evaluar_modelo.py', 'evaluacion.ipynb')
