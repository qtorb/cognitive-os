# 📤 Exportación y Configuración de IA — Cognitive OS

## ✨ Características Implementadas

### 1️⃣ Exportación a JSON

**Endpoints:**

```
GET /export/decisions
  → Exporta TODAS las decisiones + análisis + patrones del usuario
  → Formato: JSON completo con timestamp de exportación
  → Requiere: Token de autenticación

GET /export/decision/{decision_id}
  → Exporta UNA decisión específica con todos sus análisis
  → Útil para compartir decisión individual
  → Requiere: Token de autenticación

GET /export/patterns
  → Exporta SOLO los patrones descubiertos
  → Incluye: fuerza inicial vs. actual, evolución, ejemplos
  → Incluye resumen (total, promedio, fortalecidos, debilitados)
  → Requiere: Token de autenticación
```

**Ejemplo de respuesta JSON:**

```json
{
  "exported_at": "2026-04-06T19:57:00.000000",
  "user": {
    "user_id": "eba32772-f6f8-43b7-bb67-d04a2ddad508",
    "email": "user@example.com",
    "role": "Product Manager",
    "decision_areas": ["Product", "Engineering"],
    "horizon": "quarters"
  },
  "patterns": [
    {
      "id": 10,
      "title": "Bias for Action",
      "description": "Tend to move fast and iterate",
      "icon": "🚀",
      "initial_strength": 5,
      "current_strength": 7,
      "evolution": 2,
      "examples_count": 3,
      "created_at": "2026-04-06T19:56:00.000000"
    }
  ],
  "summary": {
    "total_patterns": 2,
    "avg_strength": 6.0,
    "patterns_strengthened": 1,
    "patterns_weakened": 0
  }
}
```

### 2️⃣ Exportación a PDF

**Endpoint:**

```
GET /export/pdf
  → Descarga PDF con decisiones + patrones + resumen ejecutivo
  → Formato: PDF de 3 páginas profesionales
  → Incluye: perfil, patrones, últimas decisiones
  → Requiere: Token de autenticación
```

**Contenido del PDF:**

1. **Portada** - Logo + fecha de generación
2. **Perfil del Usuario** - Email, rol, áreas, horizonte
3. **Resumen de Decisiones** - Total, completadas (%), en análisis, borradores
4. **Patrones Personales** - Lista con descripción y evolución de fuerza
5. **Últimas Decisiones** - 5 últimas decisiones con contexto
6. **Footer** - Nota de privacidad

**Ejemplo:**
```
Tamaño: ~4-5 KB
Versión: PDF 1.4
Páginas: 3 (automáticamente)
Descarga: Nombre = "Cognitive_OS_{email}_{YYYYMMDD}.pdf"
```

### 3️⃣ Configuración Model-Agnostic de IA

**Endpoints:**

```
GET /ai/config
  → Obtiene configuración actual de IA
  → Retorna: proveedor, modelo, opciones disponibles
  → No requiere autenticación (info pública)

POST /ai/config
  → Cambia proveedor y modelo de IA
  → Requiere: { "provider": "openai|anthropic|ollama", "model": "..." }
  → Retorna: instrucciones para aplicar cambios
```

**Proveedores Soportados:**

| Proveedor | Modelos | Configuración |
|-----------|---------|---------------|
| **anthropic** | claude-opus-4, claude-sonnet-4, claude-haiku | `AI_PROVIDER=anthropic`<br/>`AI_MODEL=claude-sonnet-4-20250514` |
| **openai** | gpt-4o, gpt-4, gpt-4-turbo, gpt-3.5-turbo | `AI_PROVIDER=openai`<br/>`AI_MODEL=gpt-4o` |
| **ollama** | llama3, llama2, mistral, neural-chat | `AI_PROVIDER=ollama`<br/>`AI_PROVIDER_URL=http://localhost:11434` |

**Ejemplo de cambio:**

```bash
# GET config actual
curl http://127.0.0.1:8000/ai/config

# Retorna:
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "available_providers": ["anthropic", "openai", "ollama"],
  "note": "Cambiar variables de entorno: AI_PROVIDER, AI_MODEL"
}

# POST para cambiar
curl -X POST http://127.0.0.1:8000/ai/config \
  -H "Content-Type: application/json" \
  -d '{"provider":"openai","model":"gpt-4o"}'

# Retorna instrucciones:
{
  "status": "config_instructions",
  "steps": [
    "1. Detén el backend (Ctrl+C)",
    "2. Exporta: export AI_PROVIDER=openai",
    "3. Exporta: export AI_MODEL=gpt-4o",
    "4. Reinicia: python main.py"
  ]
}
```

## 🏗️ Arquitectura Técnica

### Módulo de Exportación (export_service.py)

```python
# Función principal
def generate_export_pdf(user: User, db: Session) -> bytes:
    """Genera PDF completo con decisiones y patrones."""
    # 1. Obtiene datos de BD
    # 2. Crea documento ReportLab
    # 3. Formatea con estilos profesionales
    # 4. Retorna bytes PDF
```

### Endpoints en main.py

- `GET /export/decisions` - JSON todas las decisiones
- `GET /export/decision/{id}` - JSON una decisión
- `GET /export/patterns` - JSON patrones
- `GET /export/pdf` - PDF profesional con descarga
- `GET /ai/config` - Obtener config actual
- `POST /ai/config` - Cambiar proveedor/modelo

## ✅ Casos de Uso

### 1. Usuario quiere compartir análisis
```
→ GET /export/pdf
→ Descarga PDF profesional
→ Comparte con stakeholders
```

### 2. Usuario quiere hacer backup
```
→ GET /export/decisions (JSON)
→ Guarda JSON localmente
→ Porta decisiones a otro sistema
```

### 3. Usuario prefiere GPT-4 en lugar de Claude
```
→ POST /ai/config { "provider": "openai", "model": "gpt-4o" }
→ Sigue instrucciones
→ Reinicia backend
→ Próximos análisis usan GPT-4
```

### 4. Usuario corre Ollama localmente
```
→ POST /ai/config { "provider": "ollama", "model": "llama3" }
→ Backend apunta a localhost:11434
→ Análisis sin conexión a internet
```

## 📊 Pruebas de Validación

```
✅ Exportación JSON: 761 bytes, 2 patrones
✅ Patrones JSON: 2 patrones exportados
✅ PDF descargado: 4,411 bytes, PDF 1.4, 3 páginas
✅ Config IA: Obtiene anthropic/claude-sonnet-4-20250514
✅ Config IA: Cambia a openai/gpt-4o
```

## 🔒 Seguridad

- ✅ Todos los endpoints de exportación requieren autenticación
- ✅ Datos JSON incluyen timestamp para auditabilidad
- ✅ PDF generado con layout profesional (sin datos sensibles expuestos)
- ✅ Config IA es pública (no hay secretos en la respuesta)

## 🚀 Futuras Mejoras

1. **Exportación CSV** - Para análisis en Excel
2. **Cambio de modelo en runtime** - Sin reinicio (guardar en DB)
3. **Plantillas de PDF personalizadas** - Usuario elige diseño
4. **Exportación compartida** - Links públicos seguros con expiración
5. **Alertas de cambio** - Notificar cuando modelo cambia

## 📝 Notas Técnicas

- **PDF Library:** ReportLab (3508+ bytes mín.)
- **Importación:** `from export_service import generate_export_pdf`
- **Response Type:** Response (no StreamingResponse)
- **Formato descarga:** `Cognitive_OS_{email}_{YYYYMMDD}.pdf`
- **Variables de entorno:** `AI_PROVIDER`, `AI_MODEL`

---

**Status:** ✅ Completamente funcional y probado
**Backend:** Corriendo en http://127.0.0.1:8000
**Ready:** Producción
