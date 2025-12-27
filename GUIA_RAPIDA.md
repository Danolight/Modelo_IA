# 🚀 GUÍA RÁPIDA - FLUJO SIMPLIFICADO

## ⚡ Editar Local → Ejecutar en Colab (SÚPER FÁCIL)

### **Paso 1: Edita en tu PC**
Abre y modifica `modelo_cuba.py` en VS Code

### **Paso 2: Sincroniza con un solo comando**

**Opción A - Archivo Batch (MÁS FÁCIL):**
```cmd
sync.bat "descripción de cambios"
```

**Opción B - PowerShell:**
```powershell
# Primero, asegúrate de estar en el directorio correcto
cd d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo

# Luego ejecuta
.\sync.ps1 "descripción de cambios"
```

**Ejemplo:**
```cmd
sync.bat "agregué análisis de viento"
```

**Esto hace automáticamente:**
- ✅ Convierte `modelo_cuba.py` → `modelo1_0.ipynb`
- ✅ Sube ambos archivos a GitHub
- ✅ Listo para abrir en Colab

### **Paso 3: Ejecuta en Colab**

1. Ve a: https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb
2. Clic en **"Open in Colab"** (botón azul arriba)
3. Ejecuta las celdas (Shift+Enter)

**¡Eso es todo!** 🎉

---

## 📋 Resumen Visual

```
┌─────────────────┐
│  1. Editar .py  │  ← En VS Code (tu PC)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. sync.bat    │  ← Doble clic o desde terminal
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Open Colab  │  ← Desde GitHub
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Ejecutar ▶  │  ← En Colab
└─────────────────┘
```

---

## 🎯 Ejemplo Completo

**Escenario:** Quieres agregar una función para analizar viento

1. **En VS Code:**
   - Abres `modelo_cuba.py`
   - Agregas tu función `analizar_viento(df)`
   - Guardas (Ctrl+S)

2. **En Terminal o Explorador:**
   ```cmd
   sync.bat "agregué análisis de viento"
   ```
   O simplemente haz **doble clic** en `sync.bat` y escribe el mensaje

3. **En tu navegador:**
   - Vas a https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb
   - Clic en "Open in Colab"
   - Ejecutas las celdas
   - ¡Tu nueva función ya está disponible!

---

## 💡 Ventajas de este método

✅ **Más simple:** Solo un comando `sync.bat`  
✅ **Automático:** El .py se convierte a .ipynb solo  
✅ **Directo:** Abres el notebook desde GitHub  
✅ **Sin configuración:** No necesitas clonar nada en Colab  
✅ **Funciona siempre:** El .bat cambia al directorio correcto automáticamente

---

## 🛠️ Solución de Problemas

### **Error: "No se reconoce sync.ps1"**
**Solución:** Usa `sync.bat` en su lugar:
```cmd
sync.bat "tu mensaje"
```

O cambia al directorio correcto primero:
```powershell
cd d:\Games\Escuela\Antigravity\Modelo_IA\modelo_ia_repo
.\sync.ps1 "tu mensaje"
```

### **Error: "Python no encontrado"**
Instala Python desde: https://www.python.org/downloads/

### **Error al hacer push**
Configura Git:
```cmd
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

---

## 🎁 Bonus: Script de Inicio

Si quieres abrir PowerShell en el directorio correcto automáticamente:
```powershell
.\inicio.ps1
```

Esto te mostrará todos los comandos disponibles.

---

**¡Feliz codificación! 🌤️📊**
