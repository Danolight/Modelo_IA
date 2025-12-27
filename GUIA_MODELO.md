# 🌤️ Guía del Modelo de Predicción Meteorológica

## 📋 Descripción

Este modelo utiliza **LSTM (Long Short-Term Memory)** para predecir variables meteorológicas en múltiples horizontes temporales:
- **1 hora** (corto plazo)
- **6 horas** (mediano plazo)  
- **12 horas** (largo plazo)

### Variables Predichas
- 🌡️ **TEMP**: Temperatura
- 🌧️ **PRCP**: Precipitación
- 💧 **DEWP**: Punto de rocío
- 🌀 **SLP**: Presión a nivel del mar
- 💨 **WDSP**: Velocidad del viento

---

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
# Crear entorno
python -m venv venv_meteo

# Activar entorno
# Windows:
venv_meteo\Scripts\activate
# Linux/Mac:
source venv_meteo/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Si no tienes GPU, instala TensorFlow CPU:
```bash
pip install tensorflow-cpu
```

---

## 📂 Estructura del Proyecto

```
modelo_ia_repo/
├── data/
│   ├── Cuba_datasheet.csv          # Dataset principal
│   └── cuba_detailed.csv           # Dataset detallado (opcional)
├── models/                          # Modelos guardados (se crea automáticamente)
├── modelo_prediccion_meteorologica.py  # Código principal
├── requirements.txt                 # Dependencias
└── GUIA_MODELO.md                  # Esta guía
```

---

## 🎯 Uso del Modelo

### Ejecución Básica

```python
# Ejecutar el pipeline completo
python modelo_prediccion_meteorologica.py
```

### Uso en Google Colab

1. Sube el archivo `modelo_prediccion_meteorologica.py` a Colab
2. Cambia la configuración:
   ```python
   USE_COLAB = True  # Línea 22
   ```
3. Asegúrate de que tus datos estén en Google Drive
4. Ejecuta el notebook

### Uso Personalizado

```python
from modelo_prediccion_meteorologica import PreparadorDatos, ModeloPrediccionMeteorologica, EvaluadorModelo

# 1. Preparar datos
preparador = PreparadorDatos('data/Cuba_datasheet.csv')
X_train, X_test, y_train, y_test = preparador.preparar_pipeline_completo()

# 2. Entrenar modelo
n_variables = len(preparador.variables_disponibles)
modelo = ModeloPrediccionMeteorologica(n_variables)
modelo.entrenar_todos_horizontes(X_train, y_train)

# 3. Evaluar
evaluador = EvaluadorModelo(modelo, preparador.scaler, preparador.variables_disponibles)
evaluador.evaluar_completo(X_test, y_test)

# 4. Guardar modelo
modelo.guardar_modelos()
```

---

## 🔧 Configuración Avanzada

### Modificar Horizontes de Predicción

```python
# En la línea 28
HORIZONTES_PREDICCION = [1, 3, 6, 12, 24]  # Agregar más horizontes
```

### Cambiar Ventana Temporal

```python
# En la línea 29
VENTANA_TEMPORAL = 48  # Usar últimas 48 horas en vez de 24
```

### Ajustar Hiperparámetros

```python
# Líneas 34-37
BATCH_SIZE = 32        # Tamaño del lote
EPOCHS = 200           # Número de épocas
VALIDATION_SPLIT = 0.2 # Proporción de validación
TEST_SIZE = 0.15       # Proporción de prueba
```

### Modificar Arquitectura del Modelo

Edita el método `construir_modelo()` en la clase `ModeloPrediccionMeteorologica`:

```python
def construir_modelo(self, horizonte):
    model = Sequential([
        Input(shape=(self.ventana_temporal, self.n_variables)),
        
        # Agregar más capas LSTM
        LSTM(256, return_sequences=True),
        Dropout(0.3),
        
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        
        # Capas densas
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        
        # Salida
        Dense(self.n_variables)
    ])
    
    # Probar diferentes optimizadores
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae', 'mse']
    )
    
    return model
```

---

## 📊 Salidas del Modelo

### Archivos Generados

1. **Modelos entrenados**:
   - `modelo_meteorologico_1h.h5`
   - `modelo_meteorologico_6h.h5`
   - `modelo_meteorologico_12h.h5`

2. **Gráficos**:
   - `predicciones_1h.png` - Comparación predicción vs real
   - `predicciones_6h.png`
   - `predicciones_12h.png`
   - `entrenamiento_1h.png` - Curvas de aprendizaje
   - `entrenamiento_6h.png`
   - `entrenamiento_12h.png`

### Métricas de Evaluación

Para cada variable y horizonte se calculan:
- **MAE** (Mean Absolute Error): Error promedio absoluto
- **RMSE** (Root Mean Squared Error): Raíz del error cuadrático medio
- **R²** (Coeficiente de determinación): Calidad del ajuste (0-1)

---

## 🐛 Solución de Problemas

### Error: "TensorFlow no instalado"

```bash
pip install tensorflow
# O para CPU:
pip install tensorflow-cpu
```

### Error: "Archivo no encontrado"

Verifica que tus datos estén en la carpeta correcta:
```python
# Para local
DATA_PATH = 'data/Cuba_datasheet.csv'

# Para Colab
DATA_PATH = '/gdrive/MyDrive/Cuba_datasheet.csv'
```

### Memoria insuficiente

Reduce el tamaño del batch:
```python
BATCH_SIZE = 16  # En vez de 64
```

O reduce la ventana temporal:
```python
VENTANA_TEMPORAL = 12  # En vez de 24
```

### Modelo no converge

1. Aumenta el número de épocas:
   ```python
   EPOCHS = 200
   ```

2. Ajusta el learning rate:
   ```python
   optimizer=keras.optimizers.Adam(learning_rate=0.0001)
   ```

3. Normaliza mejor los datos (ya está implementado)

---

## 📈 Próximos Pasos

### 1. Crear la Aplicación Web

Una vez que el modelo esté entrenado, puedes crear una app web para visualizar predicciones en tiempo real.

**Tecnologías sugeridas**:
- **Backend**: Flask o FastAPI
- **Frontend**: React, Vue, o HTML/CSS/JS vanilla
- **Visualización**: Chart.js, Plotly, o D3.js

### 2. Mejorar el Modelo

- Agregar más variables (dirección del viento, nubosidad, etc.)
- Probar otras arquitecturas (GRU, Transformer)
- Implementar ensemble de modelos
- Agregar atención (Attention mechanism)

### 3. Despliegue

- Subir a Google Cloud, AWS, o Azure
- Crear API REST para predicciones
- Implementar actualización automática con nuevos datos

---

## 📚 Recursos Adicionales

### Documentación
- [TensorFlow LSTM](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)
- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Pandas Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)

### Tutoriales
- [Time Series Forecasting with LSTM](https://www.tensorflow.org/tutorials/structured_data/time_series)
- [Weather Prediction with Deep Learning](https://keras.io/examples/timeseries/)

---

## 👨‍💻 Autor

**Modelo IA Cuba**  
Fecha: 2025-12-27

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

---

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa esta guía
2. Verifica los logs de error
3. Consulta la documentación de TensorFlow
4. Abre un issue en el repositorio

---

**¡Buena suerte con tus predicciones meteorológicas! 🌤️**
