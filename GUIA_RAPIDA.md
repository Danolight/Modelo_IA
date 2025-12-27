# 🚀 GUÍA RÁPIDA - FLUJO SIMPLIFICADO

## ⚡ Editar Local → Ejecutar en Colab (SÚPER FÁCIL)

### **Paso 1: Edita en tu PC**
Abre y modifica `modelo_cuba.py` en VS Code

### **Paso 2: Sincroniza con un solo comando**
En PowerShell (desde la carpeta `modelo_ia_repo`):

```powershell
.\sync.ps1 "descripción de tus cambios"
```

Ejemplo:
```powershell
.\sync.ps1 "agregué análisis de viento"
```

**Esto hace automáticamente:**
- ✅ Convierte `modelo_cuba.py` → `modelo1_0.ipynb`
- ✅ Sube ambos archivos a GitHub
- ✅ Listo para abrir en Colab

### **Paso 3: Ejecuta en Colab**

1. Ve a: https://github.com/Danolight/Modelo_IA
2. Abre `modelo1_0.ipynb`
3. Clic en **"Open in Colab"** (botón azul arriba)
4. Ejecuta las celdas (Shift+Enter)

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
│  2. .\sync.ps1  │  ← Un solo comando
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

2. **En PowerShell:**
   ```powershell
   .\sync.ps1 "agregué análisis de viento"
   ```

3. **En tu navegador:**
   - Vas a https://github.com/Danolight/Modelo_IA/blob/base/modelo1_0.ipynb
   - Clic en "Open in Colab"
   - Ejecutas las celdas
   - ¡Tu nueva función ya está disponible!

---

## 💡 Ventajas de este método

✅ **Más simple:** Solo un comando `.\sync.ps1`  
✅ **Automático:** El .py se convierte a .ipynb solo  
✅ **Directo:** Abres el notebook desde GitHub  
✅ **Sin configuración:** No necesitas clonar nada en Colab  

---

## 🛠️ Solución de Problemas

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

---

**¡Feliz codificación! 🌤️📊**
