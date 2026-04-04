# Cognitive OS - Quickstart

## ⚡ Ejecutar en 2 minutos

### Terminal 1: Iniciar el backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Espera a ver: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Abrir el frontend

```bash
# En macOS
open onboarding.html

# En Windows (desde PowerShell)
start onboarding.html

# O simplemente abre el archivo en tu navegador
```

---

## ✅ Verificar que funciona

1. **Frontend**: `onboarding.html` debería cargar
2. **Indicador de estado**: Arriba a la derecha debería decir "Conectado" (verde)
3. **API Docs**: Abre http://127.0.0.1:8000/docs

---

## 🎯 Flujo completo

1. Completa el onboarding (rol, áreas, tipos, horizonte)
2. Presiona "Completar"
3. Los datos se envían al backend (FastAPI)
4. Se crea la BD y guarda tu perfil
5. Recibes tu `user_id` (UUID)
6. Puedes empezar a registrar decisiones

---

## 📊 Verificar que los datos se guardaron

En la API Docs (http://127.0.0.1:8000/docs):

1. Abre el endpoint `GET /user/{user_id}`
2. Pega tu user_id
3. Presiona "Try it out"

Deberías ver tu perfil completo.

---

## 🔧 Configuración

Si quieres cambiar el puerto o URL del backend, edita:

**En `onboarding.html`:**
```javascript
const API_URL = 'http://127.0.0.1:8000';  // Cambia aquí
```

**En `backend/main.py`:**
```python
uvicorn.run(app, host="127.0.0.1", port=8000)  # Cambia aquí
```

---

## 💾 Datos persistentes

- Los datos se guardan en `backend/cognitive_os.db`
- Si quieres limpiar todo: borra ese archivo y reinicia
- Los datos también se guardan en localStorage del navegador (respaldo)

---

## 📝 Próximos pasos

1. ✅ Onboarding funcionando
2. ✅ Backend persistiendo datos
3. 🔄 **Siguiente**: Dashboard para ver decisiones y registrar nuevas
4. 🔄 **Después**: Endpoints de análisis con IA

---

## 🆘 Problemas comunes

**"Sin conexión" en el indicador de estado**
- ¿Ejecutaste `python main.py`?
- ¿Está en la carpeta `/backend`?
- ¿El puerto 8000 está libre?

**"CORS error" en consola**
- Ya está resuelto (CORS habilitado)
- Si persiste, abre la consola y pega el error

**"Database is locked"**
- Cierra FastAPI y reinicia
- O borra `cognitive_os.db` (perderás datos)

**"pip: command not found"**
- Usa `pip3`
- O activa: `source venv/bin/activate` (macOS/Linux)

---

## 📞 URLs importantes

- **Frontend**: `file:///path/to/onboarding.html`
- **Backend**: `http://127.0.0.1:8000`
- **API Docs**: `http://127.0.0.1:8000/docs`
- **Health**: `http://127.0.0.1:8000/health`

---

**¡Listo! Ya tienes Cognitive OS funcionando en tu mini-pc.**
