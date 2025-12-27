# 🚀 GUÍA RÁPIDA DE USO

## ⚡ Flujo de Trabajo: Editar Local → Entrenar en Colab

### **Paso 1: Edita en tu PC**
Abre y modifica `modelo_cuba.py` en VS Code (ya lo tienes abierto)

### **Paso 2: Sube los cambios a GitHub**
En la terminal de PowerShell (desde la carpeta `modelo_ia_repo`):

```powershell
.\sync_to_colab.ps1 "descripción de tus cambios"
```

Ejemplo:
```powershell
.\sync_to_colab.ps1 "agregué función de predicción"
```

### **Paso 3: En Google Colab**

1. **Primera vez solamente:**
   ```python
   !git clone https://github.com/Danolight/Modelo_IA.git
   ```

2. **Cada vez que edites local:**
   ```python
   # Cambiar al directorio
   %cd /content/Modelo_IA
   
   # Descargar tus cambios
   !git pull origin base
   
   # Montar Drive (si necesitas los datos)
   from google.colab import drive
   drive.mount('/gdrive')
   
   # Ejecutar tu código
   %run modelo_cuba.py
   ```

---

## 📝 Comandos Útiles

### En tu PC (PowerShell):
```powershell
# Subir cambios
.\sync_to_colab.ps1 "mensaje"

# Descargar cambios desde Colab
.\sync_from_colab.ps1
```

### En Colab:
```python
# Actualizar código
!git pull origin base

# Ejecutar script completo
%run modelo_cuba.py

# O importar funciones específicas
import modelo_cuba as mc
data1, data2 = mc.cargar_datos()
```

---

## 🎯 Ejemplo Completo

**En tu PC:**
1. Editas `modelo_cuba.py` → Agregas una nueva función
2. Ejecutas: `.\sync_to_colab.ps1 "nueva función de análisis"`

**En Colab:**
```python
# Actualizar
%cd /content/Modelo_IA
!git pull origin base

# Ejecutar
%run modelo_cuba.py
```

¡Eso es todo! 🎉
