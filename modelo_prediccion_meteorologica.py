"""
Modelo de Predicción Meteorológica Multi-Horizonte
Predicción de variables meteorológicas clave en intervalos diarios
Optimizado para alta precisión y prevención de overfitting

Autor: Modelo IA Cuba
Fecha: 2025-12-27
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
import pickle
from pathlib import Path
warnings.filterwarnings('ignore')

# TensorFlow/Keras
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import (LSTM, Dense, Dropout, Input, 
                                         Bidirectional, BatchNormalization,
                                         Attention, MultiHeadAttention, LayerNormalization)
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.regularizers import l2
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️  TensorFlow no instalado. Instala con: pip install tensorflow")

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Configuración de ejecución
USE_COLAB = False  # Cambiar a True cuando ejecutes en Colab

# Rutas de datos
if USE_COLAB:
    from google.colab import drive
    drive.mount('/gdrive')
    DATA_PATH = '/gdrive/MyDrive/Cuba_datasheet.csv'
    MODELS_DIR = '/gdrive/MyDrive/modelos_meteorologicos/'
else:
    DATA_PATH = 'data_csv/Cuba_datasheet.csv'
    MODELS_DIR = 'models/'

# Crear directorio de modelos
Path(MODELS_DIR).mkdir(parents=True, exist_ok=True)

# ============================================================================
# CONFIGURACIÓN DEL MODELO - AJUSTADA SEGÚN DATOS DIARIOS
# ============================================================================

# Variables meteorológicas CLAVE (simplificado para evitar complejidad)
VARIABLES_CORE = ['TEMP', 'DEWP', 'PRCP', 'WDSP', 'MAX', 'MIN']

# Horizontes de predicción en DÍAS (datos son diarios, no interpolar)
HORIZONTES_PREDICCION = [1, 2, 3]  # 1 día, 2 días, 3 días

# Ventana temporal (días pasados para predecir)
VENTANA_TEMPORAL = 30  # Usar últimos 30 días

# Configuración de entrenamiento
BATCH_SIZE = 32
EPOCHS = 200
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.15
TEST_SIZE = 0.15

# Regularización (prevenir overfitting)
DROPOUT_RATE = 0.35
L2_REG = 0.001

# Estación meteorológica por defecto (se puede cambiar)
ESTACION_DEFAULT = 'JARDINES DEL REY, CU'

# Random seed para reproducibilidad
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
if TENSORFLOW_AVAILABLE:
    tf.random.set_seed(RANDOM_SEED)


# ============================================================================
# PARTE 1: CARGA Y PREPARACIÓN DE DATOS
# ============================================================================

class PreparadorDatos:
    """
    Clase para cargar, limpiar y preparar datos meteorológicos
    Optimizada para prevenir overfitting y maximizar generalización
    """
    
    def __init__(self, ruta_datos, estacion=ESTACION_DEFAULT):
        """
        Inicializa el preparador de datos
        
        Args:
            ruta_datos: Ruta al archivo CSV
            estacion: Nombre de la estación meteorológica a usar
        """
        self.ruta_datos = ruta_datos
        self.estacion = estacion
        self.df_original = None
        self.df_limpio = None
        self.df_procesado = None
        self.scaler = RobustScaler()  # Más robusto a outliers que MinMaxScaler
        self.imputer = KNNImputer(n_neighbors=5)
        self.variables_seleccionadas = []
        
    def cargar_datos(self):
        """Carga los datos desde el CSV"""
        print("="*70)
        print("📂 CARGANDO DATOS METEOROLÓGICOS")
        print("="*70)
        
        self.df_original = pd.read_csv(self.ruta_datos)
        print(f"✅ Datos cargados: {self.df_original.shape[0]:,} registros")
        print(f"📊 Columnas: {list(self.df_original.columns)}")
        
        # Mostrar estaciones disponibles
        if 'NAME' in self.df_original.columns:
            estaciones = self.df_original['NAME'].unique()
            print(f"\n🌍 Estaciones disponibles ({len(estaciones)}):")
            for i, est in enumerate(estaciones[:10], 1):
                count = len(self.df_original[self.df_original['NAME'] == est])
                print(f"  {i}. {est}: {count:,} registros")
            if len(estaciones) > 10:
                print(f"  ... y {len(estaciones) - 10} más")
        
        return self.df_original
    
    def filtrar_estacion(self):
        """Filtra datos por estación meteorológica específica"""
        print(f"\n🎯 Filtrando datos para estación: {self.estacion}")
        
        if 'NAME' not in self.df_original.columns:
            print("⚠️  Columna 'NAME' no encontrada. Usando todos los datos.")
            df_estacion = self.df_original.copy()
        else:
            df_estacion = self.df_original[self.df_original['NAME'] == self.estacion].copy()
            
            if len(df_estacion) == 0:
                print(f"⚠️  No se encontraron datos para '{self.estacion}'")
                print("📍 Usando la estación con más datos...")
                estacion_max = self.df_original['NAME'].value_counts().idxmax()
                df_estacion = self.df_original[self.df_original['NAME'] == estacion_max].copy()
                self.estacion = estacion_max
                print(f"✅ Usando: {self.estacion}")
        
        print(f"✅ Registros filtrados: {len(df_estacion):,}")
        return df_estacion
    
    def limpiar_datos(self, df):
        """
        Limpia datos eliminando valores centinela y procesando fechas
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            DataFrame limpio
        """
        print("\n🧹 LIMPIANDO DATOS")
        print("="*70)
        
        df_clean = df.copy()
        
        # Convertir fecha a datetime
        if 'DATE' in df_clean.columns:
            df_clean['DATE'] = pd.to_datetime(df_clean['DATE'])
            df_clean = df_clean.sort_values('DATE').reset_index(drop=True)
            print(f"📅 Período: {df_clean['DATE'].min()} a {df_clean['DATE'].max()}")
        
        # Reemplazar valores centinela por NaN
        valores_centinela = [999.9, 9999.9, 99.99, -9999]
        
        for col in df_clean.select_dtypes(include=[np.number]).columns:
            df_clean[col] = df_clean[col].replace(valores_centinela, np.nan)
        
        # Analizar valores faltantes
        print("\n📉 Análisis de valores faltantes:")
        missing_pct = (df_clean.isnull().sum() / len(df_clean) * 100).sort_values(ascending=False)
        
        for col, pct in missing_pct.items():
            if pct > 0:
                print(f"  {col}: {pct:.1f}%")
        
        # Eliminar columnas con >70% de datos faltantes
        columnas_eliminar = missing_pct[missing_pct > 70].index.tolist()
        if columnas_eliminar:
            print(f"\n🗑️  Eliminando columnas con >70% faltantes: {columnas_eliminar}")
            df_clean = df_clean.drop(columns=columnas_eliminar)
        
        self.df_limpio = df_clean
        return df_clean
    
    def seleccionar_variables_core(self, df):
        """
        Selecciona solo las variables meteorológicas CLAVE
        
        Args:
            df: DataFrame limpio
            
        Returns:
            DataFrame con variables seleccionadas
        """
        print("\n🎯 SELECCIONANDO VARIABLES CORE")
        print("="*70)
        
        # Verificar qué variables están disponibles
        vars_disponibles = [v for v in VARIABLES_CORE if v in df.columns]
        vars_faltantes = [v for v in VARIABLES_CORE if v not in df.columns]
        
        if vars_faltantes:
            print(f"⚠️  Variables no disponibles: {vars_faltantes}")
        
        print(f"✅ Variables seleccionadas: {vars_disponibles}")
        self.variables_seleccionadas = vars_disponibles
        
        # Crear DataFrame con DATE + variables
        df_vars = df[['DATE'] + vars_disponibles].copy()
        
        return df_vars
    
    def crear_features_temporales(self, df):
        """
        Crea características temporales cíclicas y de tendencia
        
        Args:
            df: DataFrame con columna DATE
            
        Returns:
            DataFrame con features adicionales
        """
        print("\n🔧 CREANDO FEATURES TEMPORALES")
        print("="*70)
        
        df_feat = df.copy()
        
        # Features cíclicas (sin data leakage)
        df_feat['day_of_year'] = df_feat['DATE'].dt.dayofyear
        df_feat['month'] = df_feat['DATE'].dt.month
        df_feat['day_of_week'] = df_feat['DATE'].dt.dayofweek
        
        # Encoding cíclico (mejor que one-hot para series temporales)
        df_feat['day_sin'] = np.sin(2 * np.pi * df_feat['day_of_year'] / 365.25)
        df_feat['day_cos'] = np.cos(2 * np.pi * df_feat['day_of_year'] / 365.25)
        df_feat['month_sin'] = np.sin(2 * np.pi * df_feat['month'] / 12)
        df_feat['month_cos'] = np.cos(2 * np.pi * df_feat['month'] / 12)
        
        # Estacionalidad
        df_feat['season'] = df_feat['month'].apply(lambda x: 
            0 if x in [12, 1, 2] else  # Invierno
            1 if x in [3, 4, 5] else   # Primavera
            2 if x in [6, 7, 8] else   # Verano
            3)  # Otoño
        
        print(f"✅ Features temporales creadas: day_sin, day_cos, month_sin, month_cos, season")
        
        return df_feat
    
    def imputar_valores_faltantes(self, df):
        """
        Imputa valores faltantes usando KNN (más inteligente que interpolación)
        
        Args:
            df: DataFrame con valores faltantes
            
        Returns:
            DataFrame sin valores faltantes
        """
        print("\n🔄 IMPUTANDO VALORES FALTANTES")
        print("="*70)
        
        # Separar DATE y columnas numéricas
        date_col = df['DATE']
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Contar NaN antes
        nan_antes = df[numeric_cols].isnull().sum().sum()
        
        if nan_antes > 0:
            print(f"📊 Valores faltantes: {nan_antes}")
            
            # Imputar con KNN
            df_imputed = df.copy()
            df_imputed[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])
            
            # Verificar
            nan_despues = df_imputed[numeric_cols].isnull().sum().sum()
            print(f"✅ Valores imputados: {nan_antes - nan_despues}")
            
            if nan_despues > 0:
                print(f"⚠️  Quedan {nan_despues} NaN. Rellenando con forward fill...")
                df_imputed = df_imputed.fillna(method='ffill').fillna(method='bfill')
        else:
            print("✅ No hay valores faltantes")
            df_imputed = df.copy()
        
        return df_imputed
    
    def normalizar_datos(self, df):
        """
        Normaliza datos usando RobustScaler (resistente a outliers)
        
        Args:
            df: DataFrame a normalizar
            
        Returns:
            DataFrame normalizado
        """
        print("\n📏 NORMALIZANDO DATOS")
        print("="*70)
        
        # Separar DATE y variables a normalizar
        date_col = df['DATE']
        
        # Solo normalizar las variables meteorológicas core
        cols_normalizar = self.variables_seleccionadas
        cols_no_normalizar = [c for c in df.columns if c not in cols_normalizar and c != 'DATE']
        
        # Normalizar
        df_norm = df.copy()
        df_norm[cols_normalizar] = self.scaler.fit_transform(df[cols_normalizar])
        
        print(f"✅ Variables normalizadas: {cols_normalizar}")
        print(f"📊 Variables sin normalizar (features): {cols_no_normalizar}")
        
        self.df_procesado = df_norm
        return df_norm
    
    def crear_secuencias_temporales(self, df, ventana=VENTANA_TEMPORAL, 
                                    horizontes=HORIZONTES_PREDICCION):
        """
        Crea secuencias temporales para LSTM
        
        Args:
            df: DataFrame normalizado
            ventana: Días pasados a usar
            horizontes: Días futuros a predecir
            
        Returns:
            X, y_dict, fechas
        """
        print("\n🔨 CREANDO SECUENCIAS TEMPORALES")
        print("="*70)
        print(f"  Ventana: {ventana} días")
        print(f"  Horizontes: {horizontes} días")
        
        # Obtener solo columnas numéricas (excluir DATE)
        datos = df.drop(columns=['DATE']).values
        fechas = df['DATE'].values
        
        X = []
        y = {h: [] for h in horizontes}
        fechas_pred = []
        
        # Crear secuencias
        max_horizonte = max(horizontes)
        
        for i in range(len(datos) - ventana - max_horizonte + 1):
            # Secuencia de entrada
            X.append(datos[i:i + ventana])
            
            # Valores objetivo para cada horizonte (solo variables core)
            n_vars_core = len(self.variables_seleccionadas)
            for h in horizontes:
                # Solo predecir las variables core (primeras n_vars_core columnas)
                y[h].append(datos[i + ventana + h - 1, :n_vars_core])
            
            fechas_pred.append(fechas[i + ventana])
        
        X = np.array(X)
        y = {h: np.array(y[h]) for h in horizontes}
        fechas_pred = np.array(fechas_pred)
        
        print(f"\n✅ Secuencias creadas:")
        print(f"  X shape: {X.shape} (muestras, ventana, features)")
        for h in horizontes:
            print(f"  y[{h}d] shape: {y[h].shape} (muestras, variables_core)")
        print(f"  Fechas: {len(fechas_pred)}")
        
        return X, y, fechas_pred
    
    def dividir_datos_temporal(self, X, y, fechas, test_size=TEST_SIZE, val_size=VALIDATION_SPLIT):
        """
        Divide datos respetando orden temporal (CRÍTICO para series temporales)
        
        Args:
            X: Secuencias de entrada
            y: Dictionary con salidas
            fechas: Array de fechas
            test_size: Proporción de test
            val_size: Proporción de validación
            
        Returns:
            X_train, X_val, X_test, y_train, y_val, y_test, fechas_train, fechas_val, fechas_test
        """
        print("\n✂️  DIVIDIENDO DATOS (DIVISIÓN TEMPORAL)")
        print("="*70)
        
        n_total = len(X)
        n_test = int(n_total * test_size)
        n_val = int(n_total * val_size)
        n_train = n_total - n_test - n_val
        
        # División temporal (no aleatoria!)
        X_train = X[:n_train]
        X_val = X[n_train:n_train + n_val]
        X_test = X[n_train + n_val:]
        
        y_train = {h: y[h][:n_train] for h in y.keys()}
        y_val = {h: y[h][n_train:n_train + n_val] for h in y.keys()}
        y_test = {h: y[h][n_train + n_val:] for h in y.keys()}
        
        fechas_train = fechas[:n_train]
        fechas_val = fechas[n_train:n_train + n_val]
        fechas_test = fechas[n_train + n_val:]
        
        print(f"✅ División completada:")
        print(f"  Train: {n_train:,} ({n_train/n_total*100:.1f}%) - {fechas_train[0]} a {fechas_train[-1]}")
        print(f"  Val:   {n_val:,} ({n_val/n_total*100:.1f}%) - {fechas_val[0]} a {fechas_val[-1]}")
        print(f"  Test:  {n_test:,} ({n_test/n_total*100:.1f}%) - {fechas_test[0]} a {fechas_test[-1]}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test, fechas_train, fechas_val, fechas_test
    
    def preparar_pipeline_completo(self):
        """
        Ejecuta todo el pipeline de preparación
        
        Returns:
            X_train, X_val, X_test, y_train, y_val, y_test, fechas_train, fechas_val, fechas_test
        """
        print("\n" + "="*70)
        print("🚀 INICIANDO PIPELINE DE PREPARACIÓN DE DATOS")
        print("="*70)
        
        # 1. Cargar
        self.cargar_datos()
        
        # 2. Filtrar por estación
        df_estacion = self.filtrar_estacion()
        
        # 3. Limpiar
        df_limpio = self.limpiar_datos(df_estacion)
        
        # 4. Seleccionar variables core
        df_vars = self.seleccionar_variables_core(df_limpio)
        
        # 5. Crear features temporales
        df_feat = self.crear_features_temporales(df_vars)
        
        # 6. Imputar valores faltantes
        df_imputed = self.imputar_valores_faltantes(df_feat)
        
        # 7. Normalizar
        df_norm = self.normalizar_datos(df_imputed)
        
        # 8. Crear secuencias
        X, y, fechas = self.crear_secuencias_temporales(df_norm)
        
        # 9. Dividir datos
        result = self.dividir_datos_temporal(X, y, fechas)
        
        print("\n" + "="*70)
        print("✅ PREPARACIÓN DE DATOS COMPLETADA")
        print("="*70)
        
        return result
    
    def guardar_preprocessors(self, ruta=MODELS_DIR):
        """Guarda scaler e imputer para uso posterior"""
        with open(f'{ruta}scaler_{self.estacion.replace(" ", "_")}.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        with open(f'{ruta}imputer_{self.estacion.replace(" ", "_")}.pkl', 'wb') as f:
            pickle.dump(self.imputer, f)
        with open(f'{ruta}variables_{self.estacion.replace(" ", "_")}.pkl', 'wb') as f:
            pickle.dump(self.variables_seleccionadas, f)
        print(f"✅ Preprocessors guardados en {ruta}")


# ============================================================================
# PARTE 2: ARQUITECTURA DEL MODELO LSTM OPTIMIZADO
# ============================================================================

class ModeloPrediccionMeteorologica:
    """
    Modelo LSTM Bidireccional con Attention para predicción multi-horizonte
    Optimizado para prevenir overfitting
    """
    
    def __init__(self, n_features, n_variables_pred, ventana=VENTANA_TEMPORAL):
        """
        Inicializa el modelo
        
        Args:
            n_features: Número total de features de entrada
            n_variables_pred: Número de variables a predecir
            ventana: Longitud de la ventana temporal
        """
        self.n_features = n_features
        self.n_variables_pred = n_variables_pred
        self.ventana = ventana
        self.modelos = {}
        self.historiales = {}
        
    def construir_modelo(self, horizonte):
        """
        Construye arquitectura LSTM Bidireccional con Attention
        
        Args:
            horizonte: Horizonte de predicción en días
            
        Returns:
            Modelo compilado
        """
        if not TENSORFLOW_AVAILABLE:
            print("❌ TensorFlow no disponible")
            return None
        
        print(f"\n🏗️  Construyendo modelo para horizonte {horizonte} días...")
        
        print(f"\n🏗️  Construyendo modelo para horizonte {horizonte} días...")
        
        # Usar API Funcional para permitir arquitectura más compleja (Attention)
        inputs = Input(shape=(self.ventana, self.n_features))
        
        # 1. Capa Bidireccional LSTM (captura contexto pasado-futuro)
        x = Bidirectional(LSTM(128, return_sequences=True, 
                              kernel_regularizer=l2(L2_REG)))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(DROPOUT_RATE)(x)
        
        # 2. Mecanismo de Atención (Self-Attention)
        # Permite al modelo enfocarse en los días más relevantes de la ventana
        # Query=x, Value=x (se atiende a sí mismo)
        atencion = MultiHeadAttention(num_heads=4, key_dim=128)(x, x)
        atencion = LayerNormalization()(atencion + x) # Conexión residual
        
        # 3. Segunda capa LSTM (procesa la secuencia ponderada)
        x = LSTM(64, return_sequences=False,
                 kernel_regularizer=l2(L2_REG))(atencion)
        x = BatchNormalization()(x)
        x = Dropout(DROPOUT_RATE)(x)
        
        # 4. Capas Densas (interpretación)
        x = Dense(64, activation='relu', kernel_regularizer=l2(L2_REG))(x)
        x = BatchNormalization()(x)
        x = Dropout(DROPOUT_RATE)(x)
        
        x = Dense(32, activation='relu', kernel_regularizer=l2(L2_REG))(x)
        x = Dropout(DROPOUT_RATE)(x)
        
        # Salida
        outputs = Dense(self.n_variables_pred)(x)
        
        # Crear modelo
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        # Compilar con Huber loss (más robusto que MSE)
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss='huber',  # Más robusto a outliers
            metrics=['mae', 'mse']
        )
        
        print(f"✅ Modelo construido para {horizonte} días (con Attention)")
        model.summary()
        
        return model
    
    def entrenar_modelo(self, X_train, y_train, X_val, y_val, horizonte):
        """
        Entrena el modelo con callbacks avanzados
        
        Args:
            X_train, y_train: Datos de entrenamiento
            X_val, y_val: Datos de validación
            horizonte: Horizonte de predicción
            
        Returns:
            Historial de entrenamiento
        """
        if not TENSORFLOW_AVAILABLE:
            print("❌ TensorFlow no disponible")
            return None
        
        print(f"\n🎯 ENTRENANDO MODELO - Horizonte {horizonte} días")
        print("="*70)
        
        # Construir modelo
        modelo = self.construir_modelo(horizonte)
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=20,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=8,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                f'{MODELS_DIR}modelo_{horizonte}d_best.h5',
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Entrenar
        historial = modelo.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=BATCH_SIZE,
            epochs=EPOCHS,
            callbacks=callbacks,
            verbose=1
        )
        
        self.modelos[horizonte] = modelo
        self.historiales[horizonte] = historial
        
        print(f"\n✅ Entrenamiento completado para {horizonte} días")
        
        return historial
    
    def entrenar_todos_horizontes(self, X_train, y_train, X_val, y_val):
        """Entrena modelos para todos los horizontes"""
        print("\n" + "="*70)
        print("🚀 ENTRENANDO MODELOS PARA TODOS LOS HORIZONTES")
        print("="*70)
        
        for horizonte in HORIZONTES_PREDICCION:
            self.entrenar_modelo(X_train, y_train[horizonte], 
                               X_val, y_val[horizonte], horizonte)
        
        print("\n" + "="*70)
        print("✅ TODOS LOS MODELOS ENTRENADOS")
        print("="*70)
    
    def guardar_modelos(self):
        """Guarda todos los modelos"""
        print("\n💾 Guardando modelos...")
        for horizonte, modelo in self.modelos.items():
            if modelo is not None:
                ruta = f'{MODELS_DIR}modelo_{horizonte}d_final.h5'
                modelo.save(ruta)
                print(f"✅ Modelo {horizonte}d guardado: {ruta}")


# ============================================================================
# PARTE 3: EVALUACIÓN Y VISUALIZACIÓN
# ============================================================================

class EvaluadorModelo:
    """Evaluación rigurosa del modelo"""
    
    def __init__(self, modelo, preparador):
        """
        Args:
            modelo: ModeloPrediccionMeteorologica entrenado
            preparador: PreparadorDatos usado
        """
        self.modelo = modelo
        self.preparador = preparador
        self.metricas = {}
        self.predicciones = {}
    
    def predecir(self, X, horizonte):
        """Realiza predicciones y desnormaliza"""
        if horizonte not in self.modelo.modelos:
            return None
        
        pred_norm = self.modelo.modelos[horizonte].predict(X, verbose=0)
        
        # Desnormalizar solo las variables core
        pred = self.preparador.scaler.inverse_transform(pred_norm)
        
        return pred
    
    def calcular_metricas(self, y_true_norm, y_pred_norm, horizonte):
        """Calcula métricas completas"""
        # Desnormalizar
        y_true = self.preparador.scaler.inverse_transform(y_true_norm)
        y_pred = self.preparador.scaler.inverse_transform(y_pred_norm)
        
        metricas = {}
        
        for i, var in enumerate(self.preparador.variables_seleccionadas):
            mae = mean_absolute_error(y_true[:, i], y_pred[:, i])
            rmse = np.sqrt(mean_squared_error(y_true[:, i], y_pred[:, i]))
            r2 = r2_score(y_true[:, i], y_pred[:, i])
            
            # MAPE (Mean Absolute Percentage Error)
            mape = np.mean(np.abs((y_true[:, i] - y_pred[:, i]) / (y_true[:, i] + 1e-8))) * 100
            
            metricas[var] = {
                'MAE': mae,
                'RMSE': rmse,
                'R²': r2,
                'MAPE': mape
            }
        
        self.metricas[horizonte] = metricas
        return metricas
    
    def mostrar_metricas(self, horizonte):
        """Muestra métricas formateadas"""
        if horizonte not in self.metricas:
            return
        
        print(f"\n{'='*70}")
        print(f"📊 MÉTRICAS - Horizonte {horizonte} días")
        print(f"{'='*70}")
        
        metricas = self.metricas[horizonte]
        
        for var in self.preparador.variables_seleccionadas:
            print(f"\n{var}:")
            print(f"  MAE:   {metricas[var]['MAE']:.4f}")
            print(f"  RMSE:  {metricas[var]['RMSE']:.4f}")
            print(f"  R²:    {metricas[var]['R²']:.4f}")
            print(f"  MAPE:  {metricas[var]['MAPE']:.2f}%")
    
    def visualizar_predicciones(self, y_true, y_pred, fechas, horizonte, n_muestras=200):
        """Visualiza predicciones vs reales"""
        n_vars = len(self.preparador.variables_seleccionadas)
        fig, axes = plt.subplots(n_vars, 1, figsize=(16, 4*n_vars))
        
        if n_vars == 1:
            axes = [axes]
        
        for i, var in enumerate(self.preparador.variables_seleccionadas):
            axes[i].plot(fechas[:n_muestras], y_true[:n_muestras, i], 
                        label='Real', alpha=0.8, linewidth=2, color='#2E86AB')
            axes[i].plot(fechas[:n_muestras], y_pred[:n_muestras, i], 
                        label='Predicción', alpha=0.8, linewidth=2, color='#A23B72')
            axes[i].set_title(f'{var} - Predicción {horizonte} días', 
                            fontsize=14, fontweight='bold')
            axes[i].set_xlabel('Fecha', fontsize=12)
            axes[i].set_ylabel(var, fontsize=12)
            axes[i].legend(fontsize=11)
            axes[i].grid(True, alpha=0.3)
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{MODELS_DIR}predicciones_{horizonte}d.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Gráfico guardado: {MODELS_DIR}predicciones_{horizonte}d.png")
    
    def visualizar_historial(self, horizonte):
        """Visualiza curvas de aprendizaje"""
        if horizonte not in self.modelo.historiales:
            return
        
        hist = self.modelo.historiales[horizonte]
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))
        
        # Loss
        axes[0].plot(hist.history['loss'], label='Train', linewidth=2)
        axes[0].plot(hist.history['val_loss'], label='Validation', linewidth=2)
        axes[0].set_title(f'Pérdida (Huber Loss) - {horizonte} días', 
                         fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Época', fontsize=12)
        axes[0].set_ylabel('Loss', fontsize=12)
        axes[0].legend(fontsize=11)
        axes[0].grid(True, alpha=0.3)
        
        # MAE
        axes[1].plot(hist.history['mae'], label='Train', linewidth=2)
        axes[1].plot(hist.history['val_mae'], label='Validation', linewidth=2)
        axes[1].set_title(f'Error Absoluto Medio (MAE) - {horizonte} días', 
                         fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Época', fontsize=12)
        axes[1].set_ylabel('MAE', fontsize=12)
        axes[1].legend(fontsize=11)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{MODELS_DIR}entrenamiento_{horizonte}d.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Gráfico guardado: {MODELS_DIR}entrenamiento_{horizonte}d.png")
    
    def evaluar_completo(self, X_test, y_test, fechas_test):
        """Evaluación completa"""
        print("\n" + "="*70)
        print("🔍 EVALUACIÓN DE MODELOS")
        print("="*70)
        
        for horizonte in HORIZONTES_PREDICCION:
            print(f"\n{'='*70}")
            print(f"Horizonte: {horizonte} días")
            print(f"{'='*70}")
            
            # Predecir
            y_pred_norm = self.modelo.modelos[horizonte].predict(X_test, verbose=0)
            
            # Calcular métricas
            self.calcular_metricas(y_test[horizonte], y_pred_norm, horizonte)
            self.mostrar_metricas(horizonte)
            
            # Desnormalizar para visualización
            y_true = self.preparador.scaler.inverse_transform(y_test[horizonte])
            y_pred = self.preparador.scaler.inverse_transform(y_pred_norm)
            
            # Visualizar
            self.visualizar_historial(horizonte)
            self.visualizar_predicciones(y_true, y_pred, fechas_test, horizonte)
            
            # Guardar predicciones
            self.predicciones[horizonte] = {'true': y_true, 'pred': y_pred}
        
        print("\n" + "="*70)
        print("✅ EVALUACIÓN COMPLETADA")
        print("="*70)


# ============================================================================
# FASES DE EJECUCIÓN (MODULAR)
# ============================================================================

def fase_1_preparacion_datos():
    """
    FASE 1: Carga, limpieza y preparación de datos
    """
    print("\n" + "="*70)
    print("🚀 FASE 1: PREPARACIÓN DE DATOS")
    print("="*70)
    
    if not TENSORFLOW_AVAILABLE:
        print("\n❌ ERROR: TensorFlow no está instalado")
        return None
    
    # Instanciar preparador
    preparador = PreparadorDatos(DATA_PATH, ESTACION_DEFAULT)
    
    # Ejecutar pipeline
    result = preparador.preparar_pipeline_completo()
    
    # Guardar preprocessors
    preparador.guardar_preprocessors()
    
    print("\n✅ FASE 1 COMPLETADA")
    return preparador, result

def fase_2_entrenamiento(preparador, datos_procesados):
    """
    FASE 2: Construcción y entrenamiento de modelos
    """
    print("\n" + "="*70)
    print("🚀 FASE 2: ENTRENAMIENTO DE MODELOS")
    print("="*70)
    
    X_train, X_val, X_test, y_train, y_val, y_test, _, _, _ = datos_procesados
    
    n_features = X_train.shape[2]
    n_variables_pred = len(preparador.variables_seleccionadas)
    
    # Instanciar modelo
    modelo = ModeloPrediccionMeteorologica(n_features, n_variables_pred)
    
    # Entrenar
    modelo.entrenar_todos_horizontes(X_train, y_train, X_val, y_val)
    
    # Guardar
    modelo.guardar_modelos()
    
    print("\n✅ FASE 2 COMPLETADA")
    return modelo

def fase_3_evaluacion_test(modelo, preparador, datos_procesados):
    """
    FASE 3: Generación de predicciones sobre conjunto de test
    """
    print("\n" + "="*70)
    print("🚀 FASE 3: TESTEO Y PREDICCIONES")
    print("="*70)
    
    _, _, X_test, _, _, y_test, _, _, fechas_test = datos_procesados
    
    # Instanciar evaluador
    evaluador = EvaluadorModelo(modelo, preparador)
    
    # Realizar predicciones y guardar internamente
    for horizonte in HORIZONTES_PREDICCION:
        print(f"  - Generando predicciones para {horizonte} días...")
        y_pred_norm = modelo.modelos[horizonte].predict(X_test, verbose=0)
        
        # Guardar en el evaluador para uso posterior
        y_true = preparador.scaler.inverse_transform(y_test[horizonte])
        y_pred = preparador.scaler.inverse_transform(y_pred_norm)
        
        evaluador.predicciones[horizonte] = {'true': y_true, 'pred': y_pred}
        
    print("\n✅ FASE 3 COMPLETADA")
    return evaluador

def fase_4_metricas_detalladas(evaluador, datos_procesados):
    """
    FASE 4: Cálculo y visualización de métricas
    """
    print("\n" + "="*70)
    print("🚀 FASE 4: MÉTRICAS DETALLADAS")
    print("="*70)
    
    _, _, _, _, _, y_test, _, _, _ = datos_procesados
    
    for horizonte in HORIZONTES_PREDICCION:
        # Recalcular métricas (o usar las guardadas si ya se hizo)
        # Aquí forzamos el cálculo para mostrarlo
        y_pred_norm = evaluador.modelo.modelos[horizonte].predict(datos_procesados[2], verbose=0)
        evaluador.calcular_metricas(y_test[horizonte], y_pred_norm, horizonte)
        evaluador.mostrar_metricas(horizonte)
        
    print("\n✅ FASE 4 COMPLETADA")

def fase_5_visualizacion_grafica(evaluador, datos_procesados):
    """
    FASE 5: Generación de gráficos
    """
    print("\n" + "="*70)
    print("🚀 FASE 5: VISUALIZACIÓN GRÁFICA")
    print("="*70)
    
    _, _, _, _, _, _, _, _, fechas_test = datos_procesados
    
    for horizonte in HORIZONTES_PREDICCION:
        print(f"\n📊 Generando gráficos para horizonte {horizonte} días...")
        
        # Recuperar predicciones
        preds = evaluador.predicciones.get(horizonte)
        if preds:
            evaluador.visualizar_historial(horizonte)
            evaluador.visualizar_predicciones(preds['true'], preds['pred'], fechas_test, horizonte)
            
    print("\n✅ FASE 5 COMPLETADA")


# ============================================================================
# EJECUCIÓN PRINCIPAL (Script)
# ============================================================================

if __name__ == "__main__":
    # Configurar visualización
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    print("\n🌤️  MODELO DE PREDICCIÓN METEOROLÓGICA (Ejecución Completa)")
    
    # Ejecutar fases secuencialmente
    preparador, datos = fase_1_preparacion_datos()
    if preparador:
        modelo = fase_2_entrenamiento(preparador, datos)
        evaluador = fase_3_evaluacion_test(modelo, preparador, datos)
        fase_4_metricas_detalladas(evaluador, datos)
        fase_5_visualizacion_grafica(evaluador, datos)
    
    print("\n🎉 EJECUCIÓN FINALIZADA")
