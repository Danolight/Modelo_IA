"""
Script para evaluar modelos pre-entrenados
Usa las mismas clases y lógica que el script de entrenamiento para garantizar consistencia.
"""

import os
import sys
from modelo_prediccion_meteorologica import (
    PreparadorDatos, 
    ModeloPrediccionMeteorologica, 
    EvaluadorModelo,
    DATA_PATH, 
    MODELS_DIR,
    HORIZONTES_PREDICCION,
    VENTANA_TEMPORAL,
    VARIABLES_CORE,
    ESTACION_DEFAULT
)

def main():
    print("="*70)
    print("EVALUACION DE MODELOS PRE-ENTRENADOS")
    print("="*70)
    print(f"Estación objetivo: {ESTACION_DEFAULT}")

    # Configuración de rutas para Colab/Local
    # Intentamos detectar si estamos en Colab o si existe la ruta de Drive
    global DATA_PATH, MODELS_DIR
    
    if os.path.exists('/gdrive/MyDrive/Cuba_datasheet.csv'):
        print("Detectado entorno Colab con Google Drive montado.")
        DATA_PATH = '/gdrive/MyDrive/Cuba_datasheet.csv'
        MODELS_DIR = '/gdrive/MyDrive/modelos_meteorologicos/'
    elif os.path.exists('Cuba_datasheet.csv'):
        DATA_PATH = 'Cuba_datasheet.csv'
        MODELS_DIR = 'models/'
        
    print(f"Usando datos en: {DATA_PATH}")
    print(f"Buscando modelos en: {MODELS_DIR}")

    # 1. Preparar Datos (Cargar CSV y Preprocessors)
    preparador = PreparadorDatos(DATA_PATH, estacion=ESTACION_DEFAULT)
    
    # Cargar datos crudos
    try:
        preparador.cargar_datos()
    except FileNotFoundError:
        print(f"\nERROR CRÍTICO: No se encuentra el archivo de datos: {DATA_PATH}")
        print("Por favor, sube 'Cuba_datasheet.csv' a tu Google Drive o directorio local.")
        return

    preparador.filtrar_estacion()
    
    # Intentar cargar preprocessors guardados
    if not preparador.cargar_preprocessors(MODELS_DIR):
        print("\n" + "!"*70)
        print("ERROR CRÍTICO: Faltan archivos de preprocesamiento (.pkl)")
        print("!"*70)
        print(f"El script buscó en: {MODELS_DIR}")
        print("Necesitas los siguientes archivos (generados durante el entrenamiento):")
        print(f"  - scaler_{preparador.estacion.replace(' ', '_')}.pkl")
        print(f"  - imputer_{preparador.estacion.replace(' ', '_')}.pkl")
        print(f"  - variables_{preparador.estacion.replace(' ', '_')}.pkl")
        print("\nSOLUCIÓN:")
        print("1. Si entrenaste en otra sesión, descarga esos archivos y súbelos a la carpeta 'modelos_meteorologicos' en tu Drive.")
        print("2. Si es la primera vez, DEBES ejecutar el entrenamiento completo primero (modelo1_0.ipynb).")
        return

    # Ejecutar pipeline de preparación (usando los preprocessors cargados)
    # NOTA: Al cargar los preprocessors, 'fit' ya está hecho.
    # Necesitamos procesar los datos para generar los sets de test.
    
    # Re-ejecutamos pasos manuales del pipeline para asegurar consistencia
    df_limpio = preparador.limpiar_datos(preparador.filtrar_estacion())
    df_vars = preparador.seleccionar_variables_core(df_limpio)
    df_feat = preparador.crear_features_temporales(df_vars)
    
    # Dividir
    df_train, df_val, df_test = preparador.dividir_datos_crudos(df_feat)
    
    # Procesar Test (Transform only)
    print("\nProcesando datos de TEST con preprocessors cargados...")
    df_test_proc = preparador.procesar_subset(df_test, fit=False)
    
    # Generar secuencias de Test
    X_test, y_test, fechas_test = preparador.crear_secuencias_temporales(df_test_proc)
    
    # 2. Cargar Modelos
    n_features = X_test.shape[2]
    n_vars_pred = len(preparador.variables_seleccionadas)
    
    modelo_wrapper = ModeloPrediccionMeteorologica(n_features, n_vars_pred)
    
    # Forzar la ruta de modelos correcta en la instancia
    # (Monkey patching temporal porque la clase usa la global MODELS_DIR por defecto)
    import modelo_prediccion_meteorologica
    modelo_prediccion_meteorologica.MODELS_DIR = MODELS_DIR
    
    modelo_wrapper.cargar_modelos_existentes()
    
    if not modelo_wrapper.modelos:
        print("\n" + "!"*70)
        print("ERROR: No se cargó ningún modelo (.h5)")
        print("!"*70)
        print(f"Buscando en: {MODELS_DIR}")
        print("Asegúrate de tener archivos como 'modelo_1d_best.h5' en esa carpeta.")
        return

    # 3. Evaluación
    evaluador = EvaluadorModelo(modelo_wrapper, preparador)
    
    print("\n" + "="*70)
    print("INICIANDO EVALUACION COMPLETA")
    print("="*70)
    
    for horizonte in HORIZONTES_PREDICCION:
        if horizonte not in modelo_wrapper.modelos:
            continue
            
        print(f"\nEvaluando horizonte {horizonte} dias...")
        
        # Predicciones
        y_pred_norm = modelo_wrapper.modelos[horizonte].predict(X_test, verbose=0)
        
        # Guardar para uso interno
        evaluador.predicciones[horizonte] = {
            'true': preparador.scaler.inverse_transform(y_test[horizonte]),
            'pred': preparador.scaler.inverse_transform(y_pred_norm)
        }
        
        # Calcular métricas
        evaluador.calcular_metricas(y_test[horizonte], y_pred_norm, horizonte)
        evaluador.mostrar_metricas(horizonte)
        
        # Visualizar Predicciones (Series temporales)
        y_true_desnorm = evaluador.predicciones[horizonte]['true']
        y_pred_desnorm = evaluador.predicciones[horizonte]['pred']
        evaluador.visualizar_predicciones(y_true_desnorm, y_pred_desnorm, fechas_test, horizonte)
        
        # Visualizar Historial (si existe el archivo history, aunque aquí cargamos pre-entrenado
        # así que no tenemos el objeto history en memoria, pero podríamos cargar el png si existe)
        # Nota: visualizar_historial requiere self.modelo.historiales que está vacío al cargar .h5
        
        # Diagnóstico de Residuos
        evaluador.visualizar_analisis_residuos(horizonte)
        
        # Reporte Automático
        evaluador.generar_diagnostico_automatico(horizonte)

    # Resumen Final
    evaluador.generar_resumen_final()

if __name__ == "__main__":
    main()
