# 🎯 Outcomes & Review System - Cognitive OS

**Fecha:** 2026-04-05
**Estado:** ✅ Implementado y funcional

---

## 🎯 Propósito

Cerrar el loop de aprendizaje en la toma de decisiones:
1. **Expectativa:** Qué esperas que pase
2. **Realidad:** Qué realmente pasó
3. **Aprendizaje:** Qué aprendiste

Este ciclo retroalimentado es crítico para que Cognitive OS sea verdaderamente educativo.

---

## 🏗️ Arquitectura

### Backend

#### Nuevos Endpoints

**POST `/decisions/{decision_id}/outcome`**
```json
{
  "outcome_real": "Descripción de lo que pasó...",
  "learnings": ["Aprendizaje 1", "Aprendizaje 2"],
  "status": "completed"  // o "reviewing"
}
```

**GET `/decisions/{decision_id}/outcome`**
```json
{
  "decision_id": 123,
  "title": "Decidir sobre nueva feature",
  "expected_outcome": "30% aumento en engagement",
  "outcome_real": "Aumento del 15% en engagement",
  "learnings": ["Subestimé la resistencia del usuario", "Los datos de beta fueron optimistas"],
  "accuracy": "partial",  // "accurate", "partial", "inaccurate"
  "status": "completed"
}
```

#### Nuevos Pydantic Models

```python
class OutcomeRecord(BaseModel):
    """Registrar qué pasó realmente con una decisión"""
    outcome_real: str
    learnings: list[str] | None = None
    status: str = "completed"

class DecisionWithOutcome(BaseModel):
    """Decisión con información completa de outcomes"""
    id: int
    title: str
    expected_outcome: str | None
    outcome_real: str | None
    learnings: list[str] | None
    accuracy: str | None  # "accurate", "partial", "inaccurate"
    status: str
```

#### Lógica de Accuracy

Analiza si el resultado fue:
- **✓ Acertado:** Contiene palabras como "éxito", "logrado", "correcto"
- **⚡ Parcial:** Contiene "parcial", "medio", "some"
- **✗ No acertado:** Resto de casos

> Futura mejora: Usar IA para evaluar accuracy de forma más sofisticada

### Frontend

#### UI Flow

1. **En Decisiones "Decided" sin outcome:**
   - Botón prominente: "🎯 Registrar resultado"

2. **En Decisiones con outcome:**
   - Botón cambia a: "📋 Ver resultado" (muestra comparación)

3. **Modal de Registro:**
   - Muestra la expectativa registrada
   - Campo para registrar lo que pasó
   - Campo para aprendizajes (multi-línea)
   - Selector de status
   - Botón guardar

4. **Modal de Comparación:**
   - Lado a lado: Esperado vs Real
   - Indicador visual de accuracy (color + texto)
   - Lista de aprendizajes
   - Hermoso diseño con boxes de colores

#### Funciones JavaScript

```javascript
// Abrir modal para registrar outcome
openOutcomeModal(decisionId, title, expectedOutcome)

// Enviar outcome al backend
handleSubmitOutcome(e)

// Cargar comparación desde backend
viewOutcomeComparison(decisionId)

// Mostrar modal de comparación
showOutcomeComparisonModal(data)
```

---

## 📊 Flujo Completo

### Paso 1: Registrar Decisión
```
Usuario: "Decidir sobre nueva feature"
Expected: "30% aumento en engagement"
Status: "draft" → "decided"
```

### Paso 2: Analizar con IA (opcional)
```
Sistema: Identifica gaps, sesgos, riesgos
Usuario: Revisa análisis
Status: "analyzing" → "decided"
```

### Paso 3: Ejecutar Decisión
```
Usuario: Implementa la decisión en el mundo real
Tiempo: Semanas/meses
Status: "decided" (esperando outcome)
```

### Paso 4: Registrar Resultado
```
Usuario: Click en "🎯 Registrar resultado"
Modal: Pide qué pasó + aprendizajes
Outcome: "15% aumento en engagement"
Learnings: ["Subestimé resistencia", "Datos beta fueron optimistas"]
Status: "completed"
```

### Paso 5: Revisión
```
Usuario: Click en "📋 Ver resultado"
Modal: Muestra comparación visual
Sistema: Detecta "parcial" (15% vs 30%)
Futuro: Estos datos alimentan Pattern Detection
```

---

## 🎨 Indicadores Visuales

### Accuracy Colors

| Resultado | Color | Ícono | HTML |
|-----------|-------|-------|------|
| Acertado | Verde | ✓ | `<span style="color: #22543d; background: #f0fff4;">✓ Acertado</span>` |
| Parcial | Naranja | ⚡ | `<span style="color: #c05621; background: #fffbf0;">⚡ Parcial</span>` |
| No acertado | Rojo | ✗ | `<span style="color: #742a2a; background: #fff5f5;">✗ No acertado</span>` |

---

## 💾 Persistencia de Datos

### Campo en Modelo Decision

```python
class Decision:
    outcome_real: Column(String, nullable=True)  # Lo que pasó
    learnings: Column(JSON, nullable=True)       # [aprendizajes]
    status: Column(String)                       # "completed", "reviewing"
```

- Los datos se guardan en SQLite
- Se recuperan en GET `/decisions/{id}/outcome`
- Se muestran en modal de comparación

---

## 🔄 Integración con Otros Sistemas

### Ideas que Muta
Cuando registras un outcome, puedes:
- Conectar nuevo learnings como Ideas
- Crear Conexiones entre la decisión y nuevas ideas
- Alimentar el ciclo cognitivo

### Alimenta Pattern Detection
El sistema de outcomes provee datos para:
- Detectar sesgos recurrentes
- Identificar qué tipo de decisiones tienes correctamente
- Entender tu proceso decisional a lo largo del tiempo

---

## 🚀 Próximas Mejoras

### Near-term
- [ ] Indicador visual en tab de "Reviewed" cuando hay outcomes
- [ ] Notificación cuando es hora de revisar (ej: después de 2 semanas)
- [ ] Bulk compare: Ver múltiples decisiones y sus outcomes

### Medium-term
- [ ] AI-powered accuracy assessment (usar Claude para evaluar)
- [ ] Pattern analysis: "70% de tus decisiones estratégicas son acertadas"
- [ ] Confidence vs Accuracy: ¿Qué tan seguro estabas vs qué tan acertado fuiste?

### Long-term
- [ ] Timeline view: Historial de todas tus decisiones y outcomes
- [ ] Seasonal patterns: Decisions tomadas en primavera vs invierno
- [ ] Decision quality score: Métrica personal de tu calidad decisional

---

## 📝 Ejemplo de Uso Completo

### Crear Decisión
```
Título: "Cambiar estrategia de marketing"
Contexto: "Campañas actuales tienen baja conversión"
Expected: "Aumentar conversión de 2% a 4%"
Conviction: 7/10
```

### Registrar Resultado (3 meses después)
```
Lo que pasó: "Conversión subió a 3.5%, mejor pero no tanto como esperábamos"
Aprendizajes:
  - El timing fue importante (lanzamos en época lenta)
  - Test A/B revealed audience prefers video over static
  - Email list quality was lower than expected
Status: "completed"
```

### Ver Comparación
```
Modal muestra:
- Esperado: 4%
- Real: 3.5%
- Accuracy: ⚡ Parcial
- Aprendizajes: [3 items]
```

---

## 🔐 Seguridad

- ✅ Autenticación JWT en todos los endpoints
- ✅ Solo usuarios pueden ver sus propios outcomes
- ✅ Validación de datos en backend
- ✅ SQL injection protegido (usando SQLAlchemy ORM)

