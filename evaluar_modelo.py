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
    VARIABLES_CORE
)

def main():
    print("="*70)
    print("EVALUACION DE MODELOS PRE-ENTRENADOS")
    print("="*70)

    # 1. Preparar Datos (Cargar CSV y Preprocessors)
    preparador = PreparadorDatos(DATA_PATH)
    
    # Cargar datos crudos
    preparador.cargar_datos()
    preparador.filtrar_estacion()
    
    # Intentar cargar preprocessors guardados
    if not preparador.cargar_preprocessors(MODELS_DIR):
        print("ERROR: No se encontraron preprocessors (scaler/imputer).")
        print("Debes haber entrenado el modelo al menos una vez para generarlos.")
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
    modelo_wrapper.cargar_modelos_existentes()
    
    if not modelo_wrapper.modelos:
        print("ERROR: No se cargó ningún modelo.")
        return

    # 3. Evaluación
    evaluador = EvaluadorModelo(modelo_wrapper, preparador)
    
    print("\n" + "="*70)
    print("INICIANDO EVALUACION")
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
        
        # Visualizar
        y_true_desnorm = evaluador.predicciones[horizonte]['true']
        y_pred_desnorm = evaluador.predicciones[horizonte]['pred']
        evaluador.visualizar_predicciones(y_true_desnorm, y_pred_desnorm, fechas_test, horizonte)
        
        # Diagnóstico
        evaluador.visualizar_analisis_residuos(horizonte)
        evaluador.generar_diagnostico_automatico(horizonte)

    # Resumen Final
    evaluador.generar_resumen_final()

if __name__ == "__main__":
    main()
