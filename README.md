# 🌤️ Modelo de Análisis Meteorológico de Cuba

Análisis de datos climáticos de estaciones meteorológicas cubanas (2004-2024)

## 📁 Estructura del Proyecto

```
Modelo_IA/
├── modelo_cuba.py              # 📝 Script principal (edita este archivo)
├── modelo1_0.ipynb             # 📓 Notebook para Colab (generado automáticamente)
├── sync.ps1                    # 🔄 Script de sincronización
├── sync_py_to_notebook.py      # 🛠️ Conversor .py → .ipynb
├── GUIA_RAPIDA.md              # 📖 Guía rápida de uso
└── README.md                   # 📄 Este archivo
```

---

## 🚀 Flujo de Trabajo Simplificado

### **Paso 1: Edita en tu PC**
Abre `modelo_cuba.py` en VS Code y haz tus cambios

### **Paso 2: Sincroniza con un comando**
```powershell
.\sync.ps1 "descripción de tus cambios"
```

### **Paso 3: Ejecuta en Colab**
1. Ve a: https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb
2. Clic en **"Open in Colab"**
3. Ejecuta las celdas

**¡Eso es todo!** 🎉

---

## 📊 Características del Script

### **Funciones Principales:**

- `cargar_datos()` - Carga los datasets de Cuba
- `explorar_datos(df)` - Muestra información básica
- `limpiar_datos(df)` - Reemplaza valores centinela por NaN
- `convertir_fechas(df)` - Convierte fechas y extrae componentes
- `analizar_temperatura(df)` - Visualizaciones de temperatura
- `analizar_precipitacion(df)` - Visualizaciones de precipitación
- `analizar_por_estacion(df)` - Comparación entre estaciones

### **Configuración Automática:**

El script detecta si está en Colab o local mediante:
```python
USE_COLAB = False  # Se cambia automáticamente a True en el notebook
```

---

## 📦 Datos

### **Dataset Principal: Cuba_datasheet.csv**
- **Registros:** 124,486
- **Período:** 2004-2024
- **Variables:** TEMP, DEWP, PRCP, SLP, WDSP, GUST, etc.

**Ubicación en Colab:** `/gdrive/MyDrive/Cuba_datasheet.csv`

---

## 🛠️ Comandos Útiles

### **Sincronización:**
```powershell
# Sincronizar cambios
.\sync.ps1 "mensaje descriptivo"
```

### **Git (si necesitas):**
```powershell
# Ver estado
git status

# Ver historial
git log --oneline

# Actualizar desde GitHub
git pull origin base
```

---

## 🎯 Ejemplo Completo

**Escenario:** Agregar análisis de viento

1. **Editas** `modelo_cuba.py`:
   ```python
   def analizar_viento(df):
       """Análisis de velocidad del viento"""
       plt.figure(figsize=(12, 6))
       df.groupby('year')['WDSP'].mean().plot()
       plt.title('Velocidad del Viento Promedio por Año')
       plt.show()
   ```

2. **Sincronizas**:
   ```powershell
   .\sync.ps1 "agregué análisis de viento"
   ```

3. **Ejecutas en Colab**:
   - Abres: https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb
   - Clic en "Open in Colab"
   - Ejecutas las celdas
   - ¡Tu nueva función ya está disponible!

---

## 🐛 Solución de Problemas

### **Error: "No se reconoce sync.ps1"**
Asegúrate de estar en la carpeta correcta:
```powershell
cd d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo
```

### **Error: "Python no encontrado"**
Instala Python desde: https://www.python.org/downloads/

### **Error al hacer push**
Configura Git:
```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

### **Error en Colab: "Archivo no encontrado"**
Verifica que:
1. Montaste Google Drive: `drive.mount('/gdrive')`
2. El archivo CSV está en `/gdrive/MyDrive/Cuba_datasheet.csv`

---

## 📦 Dependencias

```
numpy
pandas
matplotlib
seaborn
scipy
```

**En Colab:** Ya están instaladas  
**En local:** `pip install numpy pandas matplotlib seaborn scipy`

---

## 🎓 Próximos Pasos

- [ ] Agregar análisis de viento
- [ ] Crear modelo predictivo de temperatura
- [ ] Detectar anomalías climáticas
- [ ] Análisis de tendencias a largo plazo
- [ ] Correlaciones entre variables meteorológicas

---

## 📧 Información del Proyecto

- **Repositorio:** https://github.com/Danolight/Modelo_IA
- **Rama principal:** `base`
- **Notebook en Colab:** [Abrir modelo1_0.ipynb](https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb)

---

**¡Feliz análisis! 🌤️📊**
