# 🧠 Anatomía del Modelo Meteorológico: Guía Técnica Detallada

Este documento desglosa **cada componente** del modelo de predicción meteorológica implementado. Está diseñado para que entiendas exactamente qué hace cada línea de código, por qué se eligió esa técnica y cómo ajustarla en el futuro.

---

## 1. Arquitectura de la Red Neuronal (El "Cerebro")

El modelo utiliza una arquitectura híbrida avanzada que combina **LSTM Bidireccional** con **Mecanismos de Atención**.

### Diagrama de Flujo de Datos

```mermaid
Input (30 días, 15 features) 
      │
      ▼
[Capa 1] Bidirectional LSTM (128 unidades) ──► Captura contexto temporal completo
      │
      ▼
[Capa 2] Multi-Head Attention (4 cabezas) ───► Identifica días clave (ej: tormenta hace 3 días)
      │
      ▼
[Capa 3] LSTM (64 unidades) ─────────────────► Procesa la secuencia ponderada
      │
      ▼
[Capa 4] Dense (64) + ReLU ──────────────────► Interpretación no lineal
      │
      ▼
[Capa 5] Dense (32) + ReLU ──────────────────► Refinamiento de características
      │
      ▼
Output (6 variables) ────────────────────────► Predicción final
```

### Desglose Capa por Capa

#### 1. Input Layer `Input(shape=(30, n_features))`
- **Qué hace**: Recibe una matriz de datos.
- **Dimensión**: `30` (días de historia) × `n_features` (variables como temperatura, viento, etc.).
- **Por qué**: 30 días es suficiente para capturar ciclos lunares y patrones mensuales sin sobrecargar la memoria.

#### 2. Bidirectional LSTM `Bidirectional(LSTM(128))`
- **Qué hace**: Procesa la secuencia de tiempo en **dos direcciones**:
  1. Del día -30 al día -1 (Cronológico).
  2. Del día -1 al día -30 (Inverso).
- **Por qué**: A diferencia de una LSTM normal que solo ve el pasado, la bidireccional "entiende" el contexto completo de la ventana. Es fundamental para detectar patrones complejos como frentes fríos que evolucionan gradualmente.
- **Configuración**: `return_sequences=True` (pasa la secuencia completa a la siguiente capa, no solo el resultado final).

#### 3. Multi-Head Attention `MultiHeadAttention(num_heads=4)`
- **Qué hace**: Es la "joya" del modelo. Permite a la red asignar **pesos de importancia** a diferentes días.
- **Ejemplo**: Si quiere predecir lluvia para mañana, el mecanismo de atención podría darle mucho peso (importancia) a la caída de presión de ayer, e ignorar la temperatura de hace 20 días.
- **Por qué**: Mejora drásticamente la capacidad del modelo para filtrar ruido y centrarse en señales relevantes.
- **Residual Connection**: `LayerNormalization(atencion + x)` suma la entrada original a la salida de atención para evitar perder información.

#### 4. LSTM Secundaria `LSTM(64)`
- **Qué hace**: Toma la secuencia "enriquecida" por la atención y la comprime en un vector de características.
- **Por qué**: Reduce la dimensionalidad antes de pasar a las capas de decisión.

#### 5. Capas Densas (Dense Layers)
- **Dense(64) -> Dense(32)**: Red neuronal clásica (perceptrón multicapa).
- **Función de Activación `ReLU`**: Permite aprender relaciones no lineales complejas.
- **Por qué**: Traducen los patrones abstractos encontrados por las LSTM en valores numéricos concretos.

#### 6. Output Layer `Dense(6)`
- **Qué hace**: Genera los 6 valores finales (`TEMP`, `DEWP`, `PRCP`, `WDSP`, `MAX`, `MIN`).
- **Activación**: `Linear` (por defecto), ya que estamos prediciendo valores continuos (regresión), no probabilidades.

---

## 2. Técnicas de Robustez y Regularización (El "Sistema Inmune")

Para evitar que el modelo memorice los datos (overfitting) y asegurar que funcione bien con datos nuevos (como los de OpenWeather), implementamos:

### A. Dropout (0.35)
- **Qué es**: Durante el entrenamiento, "apaga" aleatoriamente el 35% de las neuronas en cada paso.
- **Efecto**: Obliga a la red a no depender de ninguna neurona específica. Crea un modelo más robusto y generalista.

### B. L2 Regularization (`kernel_regularizer=l2(0.001)`)
- **Qué es**: Penaliza matemáticamente a la red si usa "pesos" muy grandes.
- **Efecto**: Evita que el modelo reaccione exageradamente a pequeños cambios o ruido en los datos. Mantiene las predicciones suaves y estables.

### C. Batch Normalization
- **Qué es**: Re-ajusta los datos dentro de la red para que tengan media 0 y varianza 1.
- **Efecto**: Acelera el entrenamiento y permite usar tasas de aprendizaje más altas sin desestabilizar el modelo.

### D. Huber Loss (Función de Pérdida)
- **Qué es**: La fórmula que calcula qué tan equivocado está el modelo.
- **Por qué Huber**:
  - Si el error es pequeño, actúa como **MSE** (preciso).
  - Si el error es gigante (un outlier, como un huracán), actúa como **MAE** (lineal).
- **Beneficio**: El modelo no se "vuelve loco" tratando de ajustar un día con datos extremos o erróneos.

---

## 3. Preparación de Datos (El "Combustible")

### A. Features Cíclicas
Transformamos el tiempo lineal en círculos trigonométricos:
- `day_sin` / `day_cos`: Para que el modelo entienda que el 31 de diciembre está "cerca" del 1 de enero.
- Sin esto, el modelo pensaría que el día 365 y el día 1 están muy lejos.

### B. RobustScaler
- Usamos `RobustScaler` en lugar de `MinMaxScaler`.
- **Diferencia**: Usa la mediana y el rango intercuartil (IQR).
- **Por qué**: Si hay un día con 1000mm de lluvia (error o huracán), `MinMaxScaler` aplastaría todos los demás días a casi 0. `RobustScaler` ignora esos extremos al calcular la escala.

### C. KNN Imputer
- Para rellenar datos faltantes (NaN), no usamos el promedio simple.
- Usamos **K-Nearest Neighbors**: Busca los 5 días más parecidos en la historia y usa sus valores. Es mucho más preciso.

---

## 4. Expectativas de Rendimiento (Primer Entrenamiento)

Al entrenar el modelo por primera vez, deberías ver métricas similares a estas:

### Métricas Objetivo (Benchmark)
| Métrica | Valor Esperado (Train) | Valor Esperado (Val/Test) | Interpretación |
|---------|------------------------|---------------------------|----------------|
| **R² (Temp)** | 0.85 - 0.95 | **0.80 - 0.90** | El modelo explica el 80-90% de la variación de temperatura. |
| **R² (Lluvia)**| 0.40 - 0.60 | **0.30 - 0.50** | La lluvia es caótica y difícil de predecir. 0.40 es aceptable. |
| **MAE (Temp)** | 1.5 - 2.0 °F | **2.0 - 3.0 °F** | Error promedio de 2-3 grados. |
| **Loss** | Decreciente | Estable | Si Val Loss empieza a subir, es overfitting. |

**Nota**: Es normal que la precisión baje a medida que el horizonte aumenta (predecir a 3 días es más difícil que a 1 día).

---

## 5. Guía de Refinamiento de Hiperparámetros (Fine-Tuning)

Si el modelo no alcanza las métricas esperadas, ajusta los parámetros en este orden:

### Escenario A: Underfitting (El modelo no aprende bien)
*Síntomas: Loss alto tanto en Train como en Val. R² bajo.*

1. **Aumentar Complejidad**:
   - Sube las unidades LSTM: `128` -> `256`.
   - Agrega otra capa densa: `Dense(128)` antes de la de 64.
2. **Reducir Regularización**:
   - Baja el Dropout: `0.35` -> `0.2`.
   - Elimina `L2 Regularization`.
3. **Aumentar Ventana**:
   - Dale más historia: `30 días` -> `60 días`.

### Escenario B: Overfitting (El modelo memoriza)
*Síntomas: Train Loss muy bajo, pero Val Loss alto o subiendo. R² Train >> R² Val.*

1. **Aumentar Regularización**:
   - Sube el Dropout: `0.35` -> `0.5`.
   - Aumenta L2: `0.001` -> `0.01`.
2. **Reducir Complejidad**:
   - Baja unidades LSTM: `128` -> `64`.
   - Reduce cabezas de atención: `4` -> `2`.
3. **Más Datos**:
   - Es la mejor solución. Si puedes conseguir más años de historia, úsalos.

### Escenario C: Entrenamiento Inestable
*Síntomas: La curva de Loss salta mucho (zig-zag).*

1. **Bajar Learning Rate**:
   - Cambia `LEARNING_RATE = 0.001` a `0.0001`.
2. **Aumentar Batch Size**:
   - Cambia `32` a `64` o `128` (si tienes memoria RAM/GPU suficiente).

---

## 6. Próximos Pasos para tu App

1. **Entrenar**: Ejecuta el notebook en Colab y guarda los archivos `.h5` y `.pkl`.
2. **Backend**: Crea una API (Flask/FastAPI) que cargue estos archivos.
3. **Ciclo de Vida**:
   - Recibe datos de OpenWeather.
   - Procesa con `scaler` y crea features cíclicas.
   - Predice con `model.predict()`.
   - Des-normaliza con `scaler.inverse_transform()`.
   - Envía JSON al frontend.

¡Tienes una base de nivel profesional! 🚀
