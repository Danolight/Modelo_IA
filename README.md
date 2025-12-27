# 🌤️ Modelo de Análisis Meteorológico de Cuba

Análisis de datos climáticos de estaciones meteorológicas cubanas (2004-2024)

## 📁 Estructura del Proyecto

```
Modelo_IA/
├── modelo_cuba.py              # Script principal (edita este en local)
├── modelo_colab_sync.ipynb     # Notebook para ejecutar en Colab
├── modelo1_0.ipynb             # Notebook original
├── sync_to_colab.ps1           # Script para subir cambios a Colab
├── sync_from_colab.ps1         # Script para descargar cambios desde Colab
├── data/                       # Carpeta para datos (crear si no existe)
└── README.md                   # Este archivo
```

## 🚀 Flujo de Trabajo (Local ↔️ Colab)

### **Configuración Inicial (Solo una vez)**

#### 1. En tu PC Local:

```powershell
# Ya tienes el repositorio clonado, así que estás listo
cd d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo
```

#### 2. En Google Colab:

1. Abre el notebook: `modelo_colab_sync.ipynb`
2. Ejecuta la celda de clonación (solo primera vez):
   ```python
   !git clone https://github.com/Danolight/Modelo_IA.git
   %cd Modelo_IA
   ```
3. Monta Google Drive y asegúrate de tener los archivos CSV allí

---

### **Uso Diario**

#### ✏️ **Editar en Local y Ejecutar en Colab:**

1. **En tu PC:** Edita `modelo_cuba.py` con VS Code
2. **En tu PC:** Ejecuta el script de sincronización:
   ```powershell
   .\sync_to_colab.ps1 "Descripción de tus cambios"
   ```
   Ejemplo:
   ```powershell
   .\sync_to_colab.ps1 "Agregué análisis de viento"
   ```

3. **En Colab:** Ejecuta la celda de actualización:
   ```python
   !git pull origin main
   ```

4. **En Colab:** Ejecuta el análisis:
   ```python
   %run modelo_cuba_colab.py
   ```

#### 📥 **Traer Cambios de Colab a Local:**

Si modificaste algo en Colab y quieres traerlo a tu PC:

1. **En Colab:** Guarda los cambios en GitHub:
   ```python
   !git add .
   !git commit -m "Cambios desde Colab"
   !git push origin main
   ```

2. **En tu PC:** Descarga los cambios:
   ```powershell
   .\sync_from_colab.ps1
   ```

---

## 📊 Características del Script

### **Funciones Principales:**

- `cargar_datos()` - Carga los datasets de Cuba
- `explorar_datos(df)` - Muestra información básica del dataset
- `limpiar_datos(df)` - Reemplaza valores centinela (999.9) por NaN
- `convertir_fechas(df)` - Convierte fechas y extrae componentes
- `analizar_temperatura(df)` - Visualizaciones de temperatura
- `analizar_precipitacion(df)` - Visualizaciones de precipitación
- `analizar_por_estacion(df)` - Comparación entre estaciones

### **Configuración:**

El script detecta automáticamente si está en Colab o local mediante la variable:
```python
USE_COLAB = False  # Cambia a True en Colab
```

---

## 🛠️ Comandos Útiles

### **Git Básico:**

```powershell
# Ver estado de cambios
git status

# Ver historial de commits
git log --oneline

# Deshacer cambios locales (¡cuidado!)
git reset --hard HEAD
```

### **Sincronización Rápida:**

```powershell
# Subir cambios a Colab
.\sync_to_colab.ps1 "mensaje"

# Descargar cambios desde Colab
.\sync_from_colab.ps1
```

---

## 📦 Dependencias

```
numpy
pandas
matplotlib
seaborn
scipy
```

En Colab ya están instaladas. En local, instala con:
```powershell
pip install numpy pandas matplotlib seaborn scipy
```

---

## 📝 Datos

### **Dataset 1: Cuba_datasheet.csv**
- 124,486 registros
- Período: 2004-2024
- Variables: TEMP, DEWP, PRCP, SLP, WDSP, etc.

### **Dataset 2: (Opcional)**
- 11,857 registros
- Datos detallados de temperatura y precipitación

**Ubicación:**
- **Colab:** `/gdrive/MyDrive/Cuba_datasheet.csv`
- **Local:** `data/Cuba_datasheet.csv`

---

## 🎯 Próximos Pasos

- [ ] Agregar análisis de viento
- [ ] Crear modelo predictivo de temperatura
- [ ] Detectar anomalías climáticas
- [ ] Análisis de tendencias a largo plazo
- [ ] Correlaciones entre variables

---

## 🐛 Solución de Problemas

### **Error: "No estás en un repositorio Git"**
```powershell
cd d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo
```

### **Error: "Permission denied" al hacer push**
Configura tus credenciales de Git:
```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

### **Error: "Archivo no encontrado" en Colab**
Verifica que:
1. Montaste Google Drive
2. El archivo CSV está en la ruta correcta
3. Ejecutaste `!git pull origin main`

---

## 📧 Contacto

Proyecto creado para análisis meteorológico de Cuba.
Repositorio: https://github.com/Danolight/Modelo_IA

---

**¡Feliz análisis! 🌤️📊**
