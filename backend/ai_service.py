"""
AI Service for Cognitive OS — Model-agnostic analysis engine.

Provider adapter pattern: swap models without changing business logic.
Supported providers: anthropic, openai, ollama (add more easily).
"""

import os


# ============================================================================
# PROVIDER ADAPTERS
# ============================================================================

class BaseProvider:
    """Interface for AI providers. Implement this to add a new model."""

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        raise NotImplementedError


class AnthropicProvider(BaseProvider):
    """Claude via Anthropic API."""

    def __init__(self):
        try:
            import anthropic
            api_key = os.getenv('ANTHROPIC_API_KEY')
            self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
            self.model = os.getenv('AI_MODEL', 'claude-sonnet-4-20250514')
        except ImportError:
            self.client = None
            print("⚠️  anthropic not installed. pip install anthropic")

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        if not self.client:
            return None
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class OpenAIProvider(BaseProvider):
    """GPT via OpenAI API."""

    def __init__(self):
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            self.client = openai.OpenAI(api_key=api_key) if api_key else None
            self.model = os.getenv('AI_MODEL', 'gpt-4o')
        except ImportError:
            self.client = None

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        if not self.client:
            return None
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


class OllamaProvider(BaseProvider):
    """Local models via Ollama."""

    def __init__(self):
        self.base_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model = os.getenv('AI_MODEL', 'llama3')

    def complete(self, prompt: str, max_tokens: int = 1024) -> str:
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", None)
        except Exception:
            return None


def get_provider() -> BaseProvider:
    """
    Select AI provider based on AI_PROVIDER env var.
    Default: anthropic. Options: anthropic, openai, ollama.
    """
    provider_name = os.getenv('AI_PROVIDER', 'anthropic').lower()

    providers = {
        'anthropic': AnthropicProvider,
        'openai': OpenAIProvider,
        'ollama': OllamaProvider,
    }

    provider_class = providers.get(provider_name, AnthropicProvider)
    return provider_class()


# ============================================================================
# ANALYSIS ENGINE (business logic — provider-agnostic)
# ============================================================================

class AnalysisEngine:
    """
    Core analysis logic for Cognitive OS.
    Uses any AI provider to analyze decisions.
    """

    def __init__(self):
        self.provider = get_provider()

    def _call(self, prompt: str, max_tokens: int = 1024) -> str:
        """Call the AI provider. Returns demo response if unavailable."""
        try:
            result = self.provider.complete(prompt, max_tokens)
            if result:
                return result
        except Exception as e:
            print(f"AI provider error: {e}")
        return None

    def analyze_decision(self, decision: dict, user_context: str) -> str:
        prompt = f"""{user_context}

DECISIÓN A ANALIZAR:
Título: {decision['title']}
Contexto: {decision['context']}
Tipo: {decision['decision_type']}
Área: {decision['area']}
Convicción: {decision.get('conviction', 5)}/10

Analiza con rigor:
1. **Lagunas de información**: ¿Qué datos clave faltan?
2. **Sesgos cognitivos**: ¿Qué sesgos podrían estar presentes?
3. **Riesgos subestimados**: ¿Qué riesgos se minimizaron?
4. **Supuestos ocultos**: ¿Qué se asume que podría no ser cierto?
5. **Preguntas incómodas**: 2-3 preguntas que desafíen la decisión.

Sé conciso. Prioriza insights únicos sobre obviedades."""

        result = self._call(prompt)
        return result or self._demo("analyze", decision)

    def counterargument(self, decision: dict, user_context: str) -> str:
        prompt = f"""{user_context}

DECISIÓN A DESAFIAR:
Título: {decision['title']}
Contexto: {decision['context']}
Tipo: {decision['decision_type']}

Como devil's advocate:
1. **Hipótesis opuesta**: Argumento MÁS FUERTE contra esta decisión
2. **Supuestos frágiles**: ¿Cuál es más probable que falle?
3. **Escenarios de fracaso**: ¿En qué contextos fallaría?
4. **Evidencia ignorada**: ¿Qué datos se minimizan?
5. **Sesgo de confirmación**: ¿Qué buscaría alguien que quiere PROBAR que estás equivocado?

Cierra con: ¿Qué cambiaría tu decisión?"""

        result = self._call(prompt)
        return result or self._demo("counterargument", decision)

    def premortem(self, decision: dict, expected_outcome: str) -> str:
        prompt = f"""DECISIÓN: {decision['title']}
RESULTADO ESPERADO: {expected_outcome}

Imagina que en 6 meses esta decisión fracasa.
1. Qué salió mal específicamente
2. Causas raíz
3. Señales que se ignoraron
4. Cómo reconocerías el fallo temprano

Sé específico con ejemplos concretos."""

        result = self._call(prompt)
        return result or self._demo("premortem", decision)

    def synthesize_decision(self, analysis: str, counterargument: str, premortem: str) -> str:
        prompt = f"""ANÁLISIS COMPLETO:

ANÁLISIS: {analysis}
CONTRAARGUMENTO: {counterargument}
PRE-MORTEM: {premortem}

Sintetiza en máximo 5 puntos:
1. Problema claro
2. Opciones principales
3. Trade-offs críticos
4. Incertidumbre clave
5. Siguiente paso

Sin ruido. Directo. Accionable."""

        result = self._call(prompt, max_tokens=512)
        return result or self._demo("synthesize", {})

    def review_decision(self, decision: dict, outcome: str, expected: str) -> str:
        prompt = f"""REVISIÓN DE DECISIÓN PASADA

DECISIÓN: {decision['title']}
CONTEXTO: {decision['context']}
ESPERADO: {expected}
REAL: {outcome}

1. Compara: ¿Qué funcionó? ¿Qué no?
2. Detecta: ¿Dónde fallaron los supuestos?
3. Analiza: ¿Qué señales se ignoraron?
4. Extrae: ¿Qué aprendiste?
5. Patrón: ¿Es un sesgo recurrente?

Sé específico. Usa números si es posible."""

        result = self._call(prompt)
        return result or self._demo("review", decision)

    def detect_patterns(self, decisions: list, user_context: str) -> str:
        decisions_text = "\n".join([
            f"- {d['title']} ({d['area']}, {d['decision_type']}): {d.get('status', 'sin resultado')}"
            for d in decisions[:10]
        ])

        prompt = f"""{user_context}

HISTORIAL DE DECISIONES:
{decisions_text}

Analiza patrones:
1. **Sesgos recurrentes**: ¿Qué patrones negativos se repiten?
   - Exceso de optimismo, infraestimación de dependencias, errores de timing
   - Sobreconfianza, contexto insuficiente, ejecución pobre
2. **Fortalezas**: ¿Dónde acierta consistentemente?
3. **Puntos débiles**: ¿Dónde falla más?
4. **Clusters**: ¿Hay agrupaciones por tema?
5. **Recomendaciones accionables**: ¿Qué cambiar?

Distingue entre patrón detectado e inferencia especulativa.
Prioriza insights accionables sobre resúmenes narrativos."""

        result = self._call(prompt)
        return result or self._demo("patterns", {})

    def _demo(self, analysis_type: str, decision: dict) -> str:
        """Fallback demo responses when no AI provider is available."""
        title = decision.get('title', 'tu decisión') if decision else 'tu decisión'

        demos = {
            "analyze": f"""[MODO DEMO — Configura AI_PROVIDER y API key para análisis real]

Análisis de: {title}

Lagunas identificadas:
- Falta contexto sobre competencia
- No hay datos sobre timeline
- Supuestos sobre recursos no validados

Sesgos detectados:
- Optimismo respecto a timeline
- Confirmación: buscando datos que apoyan la idea

Preguntas incómodas:
- ¿Qué pasa si el mercado cambia?
- ¿Cuánto te afecta si esto falla?""",

            "counterargument": f"""[MODO DEMO]

Escenarios donde {title} falla:
1. El timing es incorrecto
2. No hay suficiente budget
3. Falta expertise crítica
4. Alguien ya lo hizo mejor

¿Qué cambiaría tu decisión?""",

            "premortem": """[MODO DEMO]

Si esta decisión falla en 6 meses:
1. Estimaciones demasiado optimistas
2. Cambio en la prioridad del negocio
3. Falta de adopción de usuarios

Señales tempranas a vigilar:
- Engagement bajo en primeros 2 meses
- Feedback negativo consistente""",

            "synthesize": """[MODO DEMO]

1. Problema: Decisión con fundamento pero riesgos no mitigados
2. Opciones: A) Proceder con ajustes | B) Más análisis | C) Esperar
3. Trade-offs: Rapidez vs seguridad
4. Incertidumbre: Comportamiento del mercado
5. Siguiente paso: Definir métricas clave""",

            "review": """[MODO DEMO]

Comparación: Expectativa vs Realidad
- Lo que funcionó: Ejecución más rápida
- Lo que no: Adopción más lenta

Patrón recurrente: Optimismo en timelines""",

            "patterns": """[MODO DEMO]

Sesgos recurrentes:
- Optimismo en estimaciones
- Sobreestimar capacidad
- Subestimar fricción de mercado

Fortalezas:
- Buen análisis de competencia
- Adaptabilidad a cambios

Mejoras sugeridas:
1. Multiplica timelines por 1.5x
2. Busca contraargumentos activamente
3. Valida supuestos con datos"""
        }

        return demos.get(analysis_type, "[MODO DEMO] Configura AI_PROVIDER para análisis real.")


# ============================================================================
# PUBLIC API
# ============================================================================

_engine = AnalysisEngine()

def get_analyzer():
    """Get the analysis engine instance."""
    return _engine
