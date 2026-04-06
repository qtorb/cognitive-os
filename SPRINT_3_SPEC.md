# Sprint 3: Análisis Avanzado + Experiencia del Usuario

**Duración estimada:** 2-3 sesiones
**Objetivo:** Convertir Cognitive OS de un sistema de registro a un sistema de **aprendizaje activo**

---

## 🎯 Objetivos Principales

| Característica | Valor | Esfuerzo |
|---|---|---|
| **Bias Detection System** | Identificar y alertar sobre sesgos recurrentes | Alto |
| **Conviction Accuracy Dashboard** | Mostrar si tus predicciones (conviction) son acertadas | Medio |
| **Decision Advisor** | IA sugiere decisiones basadas en tu historial | Alto |
| **Export Capabilities** | Exportar decisiones a PDF/JSON | Medio |
| **Dark Mode Persistence** | Recordar preferencia de usuario | Bajo |

---

## 📋 Feature Breakdown

### 1. **Bias Detection System** ⭐ CRÍTICA
**¿Qué hace?** Analiza todas tus decisiones y detecta patrones de sesgo.

**Ejemplo:**
```
Tu análisis reciente detectó:
- ⚠️ Sesgo de optimismo temporal (3 decisiones últimas 2 meses)
- ⚠️ Infraestimación de riesgos externos (50% de tus decisiones)
- ✅ Buen accuracy en decisiones tácticas (70%)
```

**Backend (ai_service.py):**
- Mejorar `detect_patterns()` para devolver `{ biases: [], strengths: [], recommendations: [] }`
- Patrón: buscar palabras clave en outcomes (overestimated, underestimated, etc)

**Frontend (Insights view):**
- Card: "🚨 Sesgos Detectados" con lista de sesgos + cuenta de apariciones
- Card: "✅ Fortalezas" con decisiones donde eres acertado
- Trending: Mostrar si el sesgo está mejorando o empeorando

**Tests:**
- Verificar que detect_patterns identifica sesgos correctamente
- Test que conviction_accuracy se calcula bien

---

### 2. **Conviction Accuracy Dashboard** ⭐⭐ IMPORTANTE
**¿Qué hace?** Compara tu conviction (qué tan seguro estabas) con los resultados reales.

**Ejemplo:**
```
Conviction vs Accuracy:
- Decisiones donde conviction >= 8: 60% acertadas (deberían ser >70%)
- Decisiones donde conviction 5-7: 45% acertadas (acertadas)
- Decisiones donde conviction < 5: 30% acertadas (demasiado pesimista)

Conclusión: Eres sobreconiado en decisiones de riesgo alto
```

**Backend (main.py /metrics):**
- Agregar `conviction_bins: { "8-10": { count: X, accurate: Y }, ... }`
- Calcular accuracy rate por rango de conviction

**Frontend (Review view):**
- Tabla: Conviction level vs Success rate
- Chart: Scatter plot de conviction vs accuracy

**Tests:**
- Verificar cálculo de accuracy por conviction range

---

### 3. **Decision Advisor** ⭐⭐⭐ PREMIUM
**¿Qué hace?** IA te sugiere qué podrías considerar en decisiones futuras, basado en tus patrones.

**Endpoint:** `POST /decisions/{decision_id}/advisor`
**Response:**
```json
{
  "decision_id": 123,
  "title": "Expand to Europe",
  "advisor_notes": [
    "Basado en tus decisiones anteriores de expansión:",
    "- Tienes tendencia a subestimar timeline (2/3 fueron retrasadas)",
    "- Tu conviction promedio en expansiones es 7.2 pero accuracy es 55%",
    "- Recomendación: Aumenta timeline en 30% y reduce expectations"
  ],
  "questions_to_consider": [
    "¿Has considerado los costos ocultos como hiciste en Italia?",
    "¿Qué pasaría si el mercado responde 6 meses más lento?"
  ]
}
```

**Backend (ai_service.py):**
- Nueva función `advise_decision(decision, user_history, patterns)`
- Usa patron detection + conviction accuracy para generar recomendaciones

**Frontend:**
- Botón "💡 Consejo" en decision detail view
- Modal con advisor notes

---

### 4. **Export Capabilities** ⭐ BONUS
**¿Qué hace?** Exportar decisiones a formatos portátiles.

**Backend endpoints:**
- `GET /decisions/export/pdf?filters=area:Product,status:completed`
- `GET /decisions/export/json?limit=100`

**Frontend:**
- Botón "Descargar" en decisiones/review view
- Opciones: PDF, JSON, CSV

**PDF:** Usa reportlab o weasyprint
- Título, contexto, outcome, learnings
- Formato profesional con branding

---

### 5. **Dark Mode Persistence** ✅ QUICK WIN
**¿Qué hace?** Recordar si el usuario prefiere dark mode.

**Frontend:**
```javascript
// En dashboard.html
const darkMode = localStorage.getItem('darkMode') === 'true';
if (darkMode) document.body.classList.add('dark-mode');
```

**Tests:** Verificar que localStorage funciona en dashboard

---

## 📊 Priorización Recomendada

```
P0 (Crítico) - Bias Detection + Conviction Accuracy
↓
P1 (Importante) - Decision Advisor
↓
P2 (Bonus) - Export + Dark Mode Persistence
```

---

## ✅ Definition of Done

- [ ] Todas las features implementadas
- [ ] Tests: 35+ (añadidos 5 nuevos tests)
- [ ] Zero regressions (30/30 tests anteriores pasan)
- [ ] Documentación actualizada en README
- [ ] Commit y push a GitHub

---

## 🔧 Notas Técnicas

### Patrón de IA para Advisor
```python
def advise_decision(decision, recent_decisions, accuracy_data):
    # 1. Find similar past decisions
    similar = find_similar_decisions(decision, recent_decisions)

    # 2. Extract patterns from outcomes
    patterns = extract_patterns(similar)

    # 3. Generate personalized advice
    advice = f"""
    Basado en tus {len(similar)} decisiones similares:
    - Pattern 1: {patterns['pattern1']}
    - Pattern 2: {patterns['pattern2']}

    Preguntas clave a considerar...
    """
    return advice
```

### Bias Detection Keywords
```python
NEGATIVE_OUTCOMES = ["retraso", "delay", "fracaso", "failed", "problema", "issue", ...]
ACCURACY_KEYWORDS = ["acertado", "correct", "logrado", "achieved", "en linea", "on track"]

# Calcula accuracy simple
accuracy = (positive_outcomes / total_outcomes) * 100
```

---

## 📝 Casos de Uso

**User Story 1: María quiere entender sus sesgos**
```
María ha tomado 30 decisiones. En Insights ve:
"⚠️ Sesgo de optimismo: 5 decisiones de expansión fallaron por timeline"
→ Esto la ayuda a identificar patrón y corregir
```

**User Story 2: Carlos quiere saber si es sobreconiado**
```
Carlos ve en Review Dashboard:
Conviction 9-10: 40% accuracy (vs 70% esperado)
Conviction 5-7: 60% accuracy (acertado)
→ Descubre que es demasiado confiado en decisiones riesgosas
```

**User Story 3: Ana quiere que la IA la asesore**
```
Ana está considerando nuevo proyecto.
Presiona "💡 Consejo" y ve:
"En tus últimos 3 proyectos similares, subestimaste timeline en 40%"
→ Puede ajustar su expectativa
```

---

## 🎬 Next Steps

1. Revisar esta especificación
2. Priorizar features (¿más bias detection o más advisor?)
3. Empezar con P0: Bias Detection + Conviction Accuracy
4. Iteración rápida con tests

---

**Estimado:** 6-8 horas de implementación
**Impacto:** Transforma el sistema de "registro pasivo" a "asesor activo"
