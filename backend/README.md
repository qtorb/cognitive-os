# Cognitive OS - Backend

API FastAPI para Cognitive OS.

## Instalación

### 1. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Desarrollo (con auto-reload)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Documentación de API

Una vez que el servidor esté corriendo:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Endpoints principales

### Onboarding

**POST** `/onboarding`
- Completa el onboarding y crea el perfil del usuario
- Request body:
  ```json
  {
    "role": "Fundador de SaaS",
    "decision_areas": ["Estrategia de producto", "Financiero"],
    "decision_types": ["Estratégicas", "Vitales"],
    "horizon": "1 año",
    "known_bias": "Muy optimista"
  }
  ```
- Response: `user_id` y perfil creado

### Perfil de usuario

**GET** `/user/{user_id}`
- Obtiene el perfil del usuario

### Decisiones

**POST** `/decisions?user_id=<user_id>`
- Crea una nueva decisión
- Request body:
  ```json
  {
    "title": "Decidir sobre nueva feature",
    "context": "...",
    "area": "Estrategia de producto",
    "decision_type": "Estratégica",
    "options": ["Opción A", "Opción B"],
    "conviction": 7
  }
  ```

**GET** `/decisions?user_id=<user_id>`
- Lista todas las decisiones del usuario

**GET** `/decisions/{decision_id}`
- Obtiene una decisión específica

**PATCH** `/decisions/{decision_id}`
- Actualiza una decisión

## Base de datos

- **Tipo**: SQLite
- **Archivo**: `cognitive_os.db` (se crea automáticamente)
- **Ubicación**: Raíz del directorio backend

### Tablas

1. **users** - Perfiles de usuarios
   - user_id (UUID)
   - role, decision_areas, decision_types, horizon, known_bias
   - context_prompt (generado automáticamente)

2. **decisions** - Decisiones registradas
   - Todos los campos del modelo Decision
   - Estados: draft, analyzing, decided, reviewing, completed

## Estructura del proyecto

```
backend/
├── main.py           # Aplicación FastAPI + endpoints
├── models.py         # Modelos de datos (SQLAlchemy)
├── requirements.txt  # Dependencias
├── README.md         # Este archivo
└── cognitive_os.db   # Base de datos (se crea al ejecutar)
```

## Notas

- El CORS está habilitado para permitir requests desde el frontend HTML
- La base de datos se crea automáticamente al iniciar
- En desarrollo, el servidor se reinicia automáticamente con cambios de código
- En producción, considerar cambiar a PostgreSQL

## Próximos pasos

1. Conectar el frontend HTML con estos endpoints
2. Agregar endpoints de análisis (IA)
3. Implementar autenticación
4. Agregar validaciones más robustas
