# Cognitive OS - Quick Start Demo para Amigos

**Duración total:** 10 minutos (setup + demo)
**Requisitos:** Python 3.9+, navegador moderno

---

## ⚡ Setup (3 minutos)

### Paso 1: Clonar/acceder al proyecto
```powershell
cd "C:\Users\$env:USERNAME\Documents\Claude\Projects\Cognitive OS"
```

### Paso 2: Instalar dependencias (si no estén ya)
```powershell
cd backend
pip install -r requirements.txt --break-system-packages
```

### Paso 3: Iniciar backend (Terminal 1)
```powershell
cd backend
python main.py
```

**Espera a ver:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 4: Abrir frontend en navegador (Terminal 2)
```powershell
# Opción A: Dashboard con demo user
start file:///absolute/path/to/dashboard.html

# Opción B: Onboarding nuevo
start file:///absolute/path/to/onboarding.html
```

> **Nota:** Reemplaza `/absolute/path/` con ruta real

---

## 📍 Demo User (Opción rápida: 5 minutos)

Si usas **dashboard.html**, ya hay un demo user pre-cargado:
- **Email:** demo@cognitive-os.local
- **Status:** Con 6 decisiones simuladas
- **Patrones:** 3 detectados automáticamente

No necesita login. Click en el dashboard y verás:

### Sección 1: Patrones Personales (1 min)
```
Dashboard → [último ícono] Insights
             ↓
         Baja a: "Tus patrones personales"
             ↓
         Verás: 3 patrones con fuerza actual (5/10, 6/10, 7/10)
```

**Qué mostrar:**
- Título de cada patrón
- Descripción ESPECÍFICA (no genérica)
- Fuerza actual
- Comentario: "Estos son MÍS patrones, no genéricos"

---

### Sección 2: Conviction Accuracy (1 min)
```
Dashboard → Insights
           ↓
       Baja a: "Conviction Accuracy"
           ↓
       Verás: Gráfico mostrando relación:
              - Eje X: Conviction level (1-10)
              - Eje Y: Accuracy (cuántas acertaste)
```

**Qué destacar:**
- "Mira: cuando confío 8-10, solo aciertas 60%"
- "Pero cuando confío 4-6, aciertas 80%"
- "Esto significa: confío cuando debería dudar"

---

### Sección 3: Decision Advisor (1 min)
```
Dashboard → Insights
           ↓
       Baja a: "Decision Advisor"
           ↓
       Si hay decisión sin outcome:
              Sistema sugiere decisiones similares
              + advertencias basadas en patrones
```

**Qué destacar:**
- "Aquí está una decisión similar que hiciste antes"
- "Falló. Y el patrón fue este"
- "La próxima vez, cuidado con esto"

---

### Sección 4: Edit & Evolución (1 min)
```
Dashboard → Panel de decisiones (arriba)
           ↓
       Click ✏️ en cualquier decisión
           ↓
       Modal: puedes cambiar:
              - Título
              - Conviction (1-10)
              - Status (Pending/Made/Closed)
              - Outcome Real (success/fail/partial)
           ↓
       Click SAVE
           ↓
       Patrones se ACTUALIZAN automáticamente
       Conviction Accuracy se recalcula
       Decision Advisor sugiere cosas nuevas
```

**Qué destacar:**
- "Cambio conviction de 8 a 6"
- "Patrones cambian EN TIEMPO REAL"
- "El sistema se adapta a mi realidad"

---

## 🆕 Opción: Crear tu propio onboarding (5 minutos)

Si prefieres ver el "wow moment" desde el inicio:

### Paso 1: Abre onboarding.html
```powershell
start file:///absolute/path/to/onboarding.html
```

### Paso 2: Completa el onboarding (2 minutos)
```
Screen 1: ¿Cuál es tu rol?
          → Ej: "Senior Engineer" o "Product Manager"

Screen 2: ¿Qué tipos de decisiones tomas?
          → Ej: "Technical architecture", "Hiring", "Product roadmap"

Screen 3: ¿Cuál es tu horizonte de decisiones?
          → Ej: "3-6 months", "1+ years"

Screen 4: Descríbete en 2 palabras
          → Ej: "Optimistic risk-taker"

Screen 5: AHORA: Agrega 2 decisiones reales
          - Decisión 1: Qué decidiste, con qué convicción (1-10)
          - Decisión 2: Otra decisión, otra convicción

Screen 6: AI ANALIZA
          → Espera 3-5 segundos
          → Verás: TUS patrones personales descubiertos
          → Comenta: "Wow, eso es exactamente yo"
```

### Paso 3: Completa setup
```
Click CONTINUE
→ Nombre, email (lo que sea)
→ Click FINISH
→ Serás redirigido al dashboard
```

### Paso 4: Ves TUS patrones
```
Dashboard → Insights
          ↓
      Verás 3 patrones específicos a TUS 2 decisiones
      (No genéricos de una libro)
```

---

## 🎯 Guión para el demo (Memorizar)

### Presentación inicial (30 segundos):
> "Esto NO es un chat con IA ni un gestor de tareas.
> Es un sistema que aprende de TUS decisiones y te advierte ANTES de cometer el mismo error.
> Día 1 ya genera insights. Mejora exponencialmente con el tiempo."

### Mostrando patrones (30 segundos):
> "Aquí están mis 3 patrones personales. NO son genéricos tipo 'la gente a menudo...'.
> Son específicos A MÍ. El sistema los descubrió analizando mis decisiones reales.
> Mira: 'Confundes voluntad con capacidad'. ESO ES. Me pasa todo el tiempo."

### Mostrando Conviction Accuracy (30 segundos):
> "Aquí está MI calibración. Cuando confío mucho (8-10), fallo más.
> Cuando tengo dudas (4-6), aciertas mejor.
> Esto me ayuda a entender: debo confiar MENOS en mis primeras intuiciones."

### Mostrando Decision Advisor (30 segundos):
> "La próxima decisión que tome, el sistema me avisará:
> 'Hace 3 meses tomaste similar y falló por este patrón.
> Cuidado.' Esto es PREVENCIÓN. No es consejo genérico después."

### Editando y viendo evolución (30 segundos):
> "Cambio el outcome de esta decisión.
> En tiempo real: patrones se actualizan, conviction accuracy se recalcula.
> El sistema aprende CONMIGO. No es estático."

---

## ❓ Preguntas típicas de críticos (y respuestas)

### P: "¿Esto requiere muchas decisiones para funcionar?"
**R:** "No. Día 1 con 2 decisiones ya genera patrones. Pero sí, más decisiones = más precisión. Después del mes, es muy preciso."

### P: "¿No es lo mismo que ChatGPT?"
**R:** "ChatGPT dice 'la gente a menudo...'. Esto dice 'TÚ específicamente...'. Diferencia entre consejo genérico y auto-conocimiento personal."

### P: "¿Qué pasa si cambio de proveedor de IA?"
**R:** "Fácil. El backend está desacoplado (model-agnostic). Cambio 1 línea y listo. La arquitectura fue diseñada para esto."

### P: "¿Esto funciona para [X tipo de decisión]?"
**R:** "Sí, si es recurrente. Contrataciones, inversiones, features a lanzar, negocios, relaciones. Cualquier decisión donde repites patrones."

### P: "¿Cuándo está ready para producción?"
**R:** "MVP avanzado está ready HOY. Fase 2 (exportación, gráficos, compartir) se hace en 2-3 semanas."

---

## ✅ Checklist antes de demo

- [ ] Backend running (puerto 8000)
- [ ] Dashboard/onboarding accesible en navegador
- [ ] Demo user cargado (o onboarding completo)
- [ ] Patrones visibles en Insights
- [ ] Conviction Accuracy gráfico visible
- [ ] Decision Advisor con sugerencias
- [ ] Puedo editar una decisión sin errores

---

## 🚨 Si hay problemas

### Backend no inicia
```powershell
# Verifica Python
python --version

# Verifica dependencias
pip list | Select-String fastapi, sqlalchemy, pydantic

# Si falta algo:
pip install fastapi sqlalchemy pydantic --break-system-packages
```

### Frontend no carga
```
- Usa ruta ABSOLUTA, no relativa
- Intenta con file:///C:/Users/...
- Chrome/Edge, no Internet Explorer
```

### No ve datos en dashboard
```
- Verifica que backend esté running
- Abre console del navegador (F12)
- Busca errores de API
- Verifica que email sea "demo@cognitive-os.local"
```

---

## 🎬 Duración estimada

| Parte | Tiempo |
|-------|--------|
| Setup | 3 min |
| Context pitch | 2 min |
| Demo patrones | 1 min |
| Demo conviction | 1 min |
| Demo advisor | 1 min |
| Demo edit | 1 min |
| Q&A | 5 min |
| **TOTAL** | **~14 min** |

---

**¡Listo! Ya estás preparado para impresionar a tus amigos críticos.**
