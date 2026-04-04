# Setup del Backend - Guía rápida

## Paso 1: Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

## Paso 2: Ejecutar el servidor

```bash
python main.py
```

O con reload en desarrollo:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: **http://127.0.0.1:8000**

## Paso 3: Verificar que funciona

Abre en tu navegador:
- **API Docs**: http://127.0.0.1:8000/docs
- **Health check**: http://127.0.0.1:8000/health

## Paso 4: Conectar el frontend

El archivo `onboarding.html` tiene dos modos:

### Modo 1: Simulado (sin backend)
- Funciona sin servidor
- Datos guardados en localStorage del navegador
- Perfecto para testear UI

### Modo 2: Con backend
- Requiere que FastAPI esté corriendo
- Datos persistidos en SQLite
- Recibe `user_id` del servidor

### Para activar Modo 2:

Edita el final de `onboarding.html` (función `completeOnboarding`):

```javascript
async function completeOnboarding() {
  // ... validaciones ...

  // Enviar al backend
  const response = await fetch('http://127.0.0.1:8000/onboarding', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if (result.status === 'success') {
    localStorage.setItem('userId', result.user_id);
    // ... mostrar resumen ...
  }
}
```

## Estructura de carpetas

```
Cognitive OS/
├── onboarding.html          # Frontend (sin dependencias)
├── BACKEND_SETUP.md        # Este archivo
└── backend/
    ├── main.py             # Aplicación FastAPI
    ├── models.py           # Modelos de datos
    ├── requirements.txt    # Dependencias
    ├── README.md           # Docs del backend
    └── cognitive_os.db     # Base de datos (se crea auto)
```

## APIs disponibles

### Completar onboarding
```
POST /onboarding
Content-Type: application/json

{
  "role": "Fundador de SaaS",
  "decision_areas": ["Estrategia de producto", "Financiero"],
  "decision_types": ["Estratégicas"],
  "horizon": "1 año",
  "known_bias": "Optimista"
}

Response:
{
  "status": "success",
  "user_id": "uuid-aqui",
  "profile": {...}
}
```

### Crear decisión
```
POST /decisions?user_id=uuid
Content-Type: application/json

{
  "title": "Decidir sobre X",
  "context": "Contexto...",
  "area": "Estrategia de producto",
  "decision_type": "Estratégica",
  "options": ["Opción A", "Opción B"],
  "conviction": 7
}
```

### Listar decisiones
```
GET /decisions?user_id=uuid
```

## Notas importantes

- **CORS** está habilitado (para desarrollo)
- **SQLite** se crea automáticamente
- En **Windows**, ejecuta con: `python main.py`
- En **Mac/Linux**, ejecuta con: `python3 main.py`
- El servidor usa puerto **8000** por defecto

## Troubleshooting

**Error: "pip: command not found"**
- Usa `pip3` en lugar de `pip`
- O activa el virtual env: `source venv/bin/activate`

**Error: "Port 8000 already in use"**
- Cambia el puerto en main.py: `uvicorn.run(..., port=8001)`

**SQLite locked**
- Cierra otras conexiones a la BD
- Borra `cognitive_os.db` y reinicia (perderás datos)

## Próximos pasos

1. ✅ Backend básico funcionando
2. 🔄 Conectar frontend con backend
3. ⏳ Agregar endpoints de análisis (IA)
4. 🔐 Implementar autenticación (opcional para MVP)
