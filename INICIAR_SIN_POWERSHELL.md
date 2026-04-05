# 🚀 Iniciar Cognitive OS sin PowerShell

Si no quieres usar PowerShell en Windows, simplemente **haz doble-click** en estos archivos:

---

## Opción 1: Iniciador automático (RECOMENDADO)

### Paso 1: Ejecutar el servidor
1. **Doble-click** en `arrancar.bat`
2. Se abrirá una ventana negra (la consola)
3. Espera a ver el mensaje: `Uvicorn running on http://127.0.0.1:8000`
4. **¡NO cierres esa ventana!** (es el servidor)

### Paso 2: Abrir el navegador
1. **Doble-click** en `abrir_frontend.bat`
2. Se abrirá automáticamente `onboarding.html` en tu navegador
3. Verifica que veas "Conectado" en la esquina superior derecha

---

## Opción 2: Manual (sin scripts)

Si prefieres abrir las cosas a mano:

1. **Abre el Explorador de archivos**
2. Ve a la carpeta `backend` de tu proyecto
3. **Haz Shift + botón derecho** en el espacio vacío
4. Selecciona "Abrir PowerShell aquí" (o "Abrir símbolo del sistema")
5. Copia y pega:
   ```
   python main.py
   ```
6. Espera el mensaje de servidor corriendo
7. En otra ventana, **abre el archivo** `onboarding.html` con tu navegador

---

## Opción 3: Acceso directo (la más cómoda)

Crea un **Acceso directo** en el Escritorio que abra `arrancar.bat`:

1. **Haz click derecho** en `arrancar.bat`
2. Selecciona "Enviar a" > "Escritorio (crear acceso directo)"
3. Ahora puedes hacer doble-click desde el escritorio

---

## 🛠️ Solucionar problemas

### "No funciona cuando hago doble-click"
- Abre la carpeta del proyecto
- Haz **Shift + click derecho** → "Abrir símbolo del sistema" o "PowerShell"
- Copia y pega manualmente:
  ```
  arrancar.bat
  ```

### "Python no se encuentra"
Prueba esto en la consola:
```
python --version
```
Si no funciona, instala Python desde [python.org](https://www.python.org/downloads/) (marca "Add Python to PATH")

### "El puerto 8000 está ocupado"
- Cierra la ventana de `arrancar.bat`
- Espera 10 segundos
- Vuelve a hacer doble-click

### "No conecta con el backend"
- Verifica que `arrancar.bat` está ejecutándose (la ventana debe estar abierta)
- Intenta ir directamente a http://127.0.0.1:8000/health en tu navegador
- Si ves un error, el servidor no está corriendo

---

## 📝 Resumen

| Tarea | Solución |
|-------|----------|
| Iniciar servidor | `arrancar.bat` (doble-click) |
| Abrir frontend | `abrir_frontend.bat` (doble-click) |
| Ver API docs | Visita http://127.0.0.1:8000/docs |
| Detener servidor | Cierra la ventana negra |

---

**¡Listo! Ahora puedes usar Cognitive OS sin PowerShell** 🎉
