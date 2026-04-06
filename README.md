# Cognitive OS — Infraestructura Cognitiva Personal

**Transforma decisiones en memoria estructurada, análisis trazable y aprendizaje acumulado.**

Cognitive OS no es un task manager, una app de notas, ni un chat genérico con IA. Es una infraestructura para pensar mejor sobre decisiones y aprender de ellas con el tiempo.

> "El chat ayuda a pensar ahora. Cognitive OS ayuda a pensar a lo largo del tiempo."

---

## El problema

Tomas cientos de decisiones al año. Aprendes de pocas. ¿Por qué?

- No registras qué creías que iba a pasar
- No comparas expectativa con realidad
- No ves los patrones en tus errores
- Repites los mismos sesgos

**Resultado:** tu criterio no mejora con la experiencia.

---

## El loop que resuelve esto

```
DECISIÓN → ANÁLISIS → OUTCOME → REVIEW → PATRÓN → SIGUIENTE DECISIÓN
```

Cada vuelta del loop acumula criterio. Ese es el producto.

---

## Qué hace (y qué no hace)

### ✅ Hace

- **Captura decisiones** con contexto, convicción esperada y outcome real
- **Analiza con IA** para identificar sesgos, riesgos y supuestos ocultos
- **Cierra el loop**: compara expectativa vs realidad y extrae aprendizajes
- **Detecta patrones personales**: tus sesgos recurrentes, tu calibración de convicción
- **Advierte antes de decidir**: "la última vez que decidiste algo similar, pasó esto"
- **Evoluciona contigo**: los patrones cambian con cada decisión registrada

### ❌ No hace

- No es un gestor de tareas
- No comparte decisiones públicamente (frozen)
- No tiene dashboard de métricas sofisticadas
- No tiene chat genérico con IA
- No necesita un servidor complejo — es un MVP local

---

## Features (Sprint 3)

### Loop principal

| Feature | Descripción |
|---------|-------------|
| **Decisiones** | CRUD con contexto, convicción 1-10, outcome esperado |
| **Análisis IA** | Gaps, sesgos cognitivos, riesgos, contraargumentos, pre-mortem |
| **Outcomes** | Registra qué pasó realmente y el aprendizaje |
| **Review** | Comparación expectativa vs realidad con análisis IA |
| **Patrones personales** | Detectados automáticamente en onboarding y actualizados con cada decisión |
| **Edición** | Decisiones y patrones editables desde el dashboard |

### Motor de aprendizaje (Sprint 3)

| Feature | Descripción |
|---------|-------------|
| **Bias Detection** | Detecta sesgos recurrentes en tus decisiones con outcomes |
| **Conviction Accuracy** | Muestra con qué precisión decides según tu nivel de confianza |
| **Decision Advisor** | Advierte cuando la decisión actual se parece a una pasada que falló |
| **Acción concreta** | Cada insight termina con una recomendación operativa específica |

### Onboarding

- Conversacional, no un formulario
- 2 decisiones reales → IA detecta 3-4 patrones personales
- "Wow moment" en el primer uso — no en semanas

---

## Stack técnico

```
Python 3.9+
FastAPI          # API central (main.py)
SQLAlchemy       # ORM
SQLite           # Base de datos local, portable
Vanilla JS       # Frontend sin frameworks
```

### Capa IA (model-agnostic)

```
AI_PROVIDER=anthropic   # claude-sonnet (default)
AI_PROVIDER=openai      # gpt-4o
AI_PROVIDER=ollama      # modelos locales
AI_MODEL=...            # configurable por env var
```

Cambiar de proveedor: 1 variable de entorno, 0 cambios de código.

### Arquitectura del ai_service.py

```
PromptBuilder   # qué preguntar — separado y tunable sin tocar lógica
Provider        # quién responde — Anthropic, OpenAI, Ollama
AnalysisEngine  # casos de uso — orquesta los dos anteriores
```

---

## Estructura

```
Cognitive OS/
├── backend/
│   ├── main.py              # FastAPI — endpoints core
│   ├── models.py            # SQLAlchemy ORM + auto-migration
│   ├── ai_service.py        # PromptBuilder + Providers + Engine
│   ├── auth.py              # JWT + Google OAuth
│   ├── export_service.py    # Export JSON/PDF
│   ├── tests.py             # Tests (24/24 ✅)
│   └── requirements.txt
├── dashboard.html           # Frontend principal
├── onboarding.html          # Onboarding conversacional
├── settings.html            # Configuración AI + export
├── arrancar.bat             # Windows: inicia backend
├── abrir_frontend.bat       # Windows: abre frontend
└── README.md                # Esta es la fuente única de verdad
```

> Los demás archivos `.md` son documentación auxiliar (demo, evaluación, testing). Este README manda.

---

## Quick Start

### Requisitos

- Python 3.9+
- Anthropic API key (o cualquier proveedor compatible)

### Instalación

```powershell
cd "Cognitive OS/backend"
pip install -r requirements.txt --break-system-packages
```

### Configurar entorno

```powershell
copy .env.example .env
```

Editar `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
JWT_SECRET=cualquier_string_random
AI_PROVIDER=anthropic
```

### Iniciar

```powershell
cd backend
python main.py
```

API en `http://localhost:8000`. Abre `dashboard.html` en el navegador.

### Windows (sin terminal)

1. Doble-click en `arrancar.bat` para iniciar el backend
2. Doble-click en `abrir_frontend.bat` para abrir el frontend

---

## Endpoints core

El sistema tiene 53 endpoints. Los que importan para el loop principal:

```
POST  /decisions                       # Crear decisión
GET   /decisions                       # Listar decisiones
PATCH /decisions/{id}                  # Editar decisión
PATCH /decisions/{id}/outcome          # Registrar resultado
GET   /decisions/{id}/outcome          # Ver comparación
POST  /decisions/{id}/analyze          # Análisis IA
POST  /decisions/{id}/counterargument  # Contraargumento
POST  /decisions/{id}/premortem        # Pre-mortem
POST  /decisions/{id}/review           # Revisión post-outcome
POST  /decisions/{id}/advisor          # Advisor (decisiones similares)
GET   /insights                        # Biases + conviction accuracy
GET   /user/{id}/patterns              # Patrones personales
PATCH /patterns/{id}                   # Editar patrón
POST  /onboarding                      # Setup inicial
GET   /health                          # Estado del servidor
```

---

## Filosofía de desarrollo

1. **¿Esto ayuda a acumular criterio en el tiempo?** Si no, no lo implementes.
2. **Claro > elegante**. Simple > abstracto. Explícito > implícito.
3. **MVP personal**: sin multiusuario, sin permisos, sin escalabilidad prematura.
4. **Model-agnostic**: la IA no es el producto, es una herramienta.
5. **Datos del usuario son suyos**: SQLite local, exportación completa, sin servers externos.

---

## Tests

```powershell
cd backend
python -m pytest tests.py -v
```

24 tests. 24 pasando. Cubre: auth, onboarding, decisions CRUD, outcomes, AI analysis, edición, edge cases.

---

## Roadmap

### ✅ Completado

- Core CRUD de decisiones
- Análisis IA (análisis, contraargumento, pre-mortem, síntesis, review)
- Outcomes y comparación expectativa vs realidad
- Pattern detection (onboarding + evolución continua)
- Bias Detection System
- Conviction Accuracy Dashboard
- Decision Advisor
- Edit functionality (decisiones y patrones)
- Onboarding conversacional con "wow moment" en día 1
- Testing completo (24/24 ✅)

### 🟡 Próximo (tighten the core)

- Reforzar flujo guiado: decisión → outcome → review → patrón
- Mejorar "motor de mejora" en Insights con más acciones concretas
- Export JSON completo del historial de decisiones

### ❄️ Congelado

- Public sharing
- Métricas avanzadas
- Nuevas capas laterales (Ideas, Connections, Reminders expansion)
- Dark mode persistence

---

**Cognitive OS: de "app de notas con IA" a "sistema que aprende de tus decisiones contigo".**
