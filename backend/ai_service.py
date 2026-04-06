"""
AI Service for Cognitive OS — Model-agnostic analysis engine.

Provider adapter pattern: swap models without changing business logic.
Supported providers: anthropic, openai, ollama (add more easily).
"""

import os
import logging


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
            logging.info("⚠️  anthropic not installed. pip install anthropic")

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
            logging.info(r"AI provider error: {e}")
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

    def analyze_decision_biases(self, decisions: list) -> dict:
        """
        Analyze decisions to detect recurring biases and strengths.
        Returns structured data instead of narrative text.
        """
        if not decisions:
            return {
                "biases": [],
                "strengths": [],
                "conviction_accuracy": None,
                "recommendations": []
            }

        # Extract data from decisions
        outcomes = []
        conviction_data = []

        for d in decisions:
            outcome_real = d.get('actual', d.get('outcome_real', ''))
            conviction = d.get('conviction')
            expected = d.get('expected', d.get('expected_outcome', ''))

            if outcome_real:
                outcomes.append({
                    'title': d.get('title', 'Decision'),
                    'expected': expected,
                    'actual': outcome_real,
                    'conviction': conviction
                })

            if conviction and outcome_real:
                conviction_data.append({
                    'conviction': conviction,
                    'outcome': outcome_real
                })

        # Detect biases from keywords in outcomes
        biases = self._extract_biases(outcomes)

        # Detect strengths (successful decisions)
        strengths = self._extract_strengths(outcomes)

        # Calculate conviction accuracy
        conviction_accuracy = self._calculate_conviction_accuracy(conviction_data)

        # Generate recommendations
        recommendations = self._generate_recommendations(biases, strengths, conviction_accuracy)

        return {
            "biases": biases,
            "strengths": strengths,
            "conviction_accuracy": conviction_accuracy,
            "recommendations": recommendations,
            "total_decisions_analyzed": len(decisions),
            "decisions_with_outcomes": len(outcomes)
        }

    def _extract_biases(self, outcomes: list) -> list:
        """Extract recurring biases from decision outcomes."""
        bias_patterns = {
            "optimismo_temporal": {
                "keywords": ["retraso", "delay", "tarde", "tardó", "tomó más tiempo"],
                "pattern": "Sesgo de optimismo temporal",
                "description": "Subestimas el tiempo que toman las cosas"
            },
            "optimismo_resultados": {
                "keywords": ["fracaso", "failed", "no funcionó", "no trabajó", "resultó peor"],
                "pattern": "Exceso de optimismo en resultados",
                "description": "Esperas mejores resultados de los que ocurren"
            },
            "infraestimacion_riesgo": {
                "keywords": ["riesgo", "problema", "issue", "complicación", "inesperado"],
                "pattern": "Infraestimación de riesgos",
                "description": "No consideras suficientemente los riesgos"
            },
            "sobreconfianza": {
                "keywords": ["sorpresa", "inesperadamente", "no esperaba", "shock"],
                "pattern": "Sobreconfianza",
                "description": "Demasiada confianza en tu predicción"
            }
        }

        detected_biases = {}

        for outcome in outcomes:
            actual_lower = outcome['actual'].lower()

            for bias_key, bias_info in bias_patterns.items():
                if any(kw in actual_lower for kw in bias_info['keywords']):
                    if bias_key not in detected_biases:
                        detected_biases[bias_key] = {
                            "type": bias_info['pattern'],
                            "description": bias_info['description'],
                            "occurrences": 0,
                            "examples": []
                        }
                    detected_biases[bias_key]['occurrences'] += 1
                    if len(detected_biases[bias_key]['examples']) < 2:
                        detected_biases[bias_key]['examples'].append(outcome['title'])

        # Convert to list, sorted by frequency
        biases = sorted(
            [
                {
                    "type": v["type"],
                    "description": v["description"],
                    "count": v["occurrences"],
                    "examples": v["examples"]
                }
                for v in detected_biases.values()
            ],
            key=lambda x: x['count'],
            reverse=True
        )

        return biases

    def _extract_strengths(self, outcomes: list) -> list:
        """Extract decision strengths (successful outcomes)."""
        success_keywords = [
            "acertado", "logrado", "éxito", "exitoso", "achieved",
            "bien", "correcto", "as expected", "expected", "cumplió"
        ]

        successes = []
        for outcome in outcomes:
            actual_lower = outcome['actual'].lower()
            if any(kw in actual_lower for kw in success_keywords):
                successes.append({
                    "title": outcome['title'],
                    "expected": outcome['expected'],
                    "actual": outcome['actual']
                })

        # Group by area or type if available
        return {
            "successful_decisions": len(successes),
            "success_rate": round((len(successes) / len(outcomes)) * 100, 1) if outcomes else 0,
            "examples": successes[:3]
        }

    def _calculate_conviction_accuracy(self, conviction_data: list) -> dict:
        """Calculate accuracy stratified by conviction level."""
        if not conviction_data:
            return None

        bins = {
            "high": {"range": (8, 10), "count": 0, "accurate": 0},
            "medium": {"range": (5, 7), "count": 0, "accurate": 0},
            "low": {"range": (1, 4), "count": 0, "accurate": 0}
        }

        success_keywords = [
            "acertado", "logrado", "éxito", "achieved", "bien", "correcto", "expected"
        ]

        for item in conviction_data:
            conviction = item['conviction']
            outcome_lower = item['outcome'].lower()
            is_accurate = any(kw in outcome_lower for kw in success_keywords)

            if conviction >= 8:
                bins["high"]["count"] += 1
                if is_accurate:
                    bins["high"]["accurate"] += 1
            elif conviction >= 5:
                bins["medium"]["count"] += 1
                if is_accurate:
                    bins["medium"]["accurate"] += 1
            else:
                bins["low"]["count"] += 1
                if is_accurate:
                    bins["low"]["accurate"] += 1

        # Calculate percentages
        result = {}
        for bin_name, bin_data in bins.items():
            if bin_data["count"] > 0:
                accuracy_pct = round((bin_data["accurate"] / bin_data["count"]) * 100, 1)
                result[bin_name] = {
                    "range": f"{bin_data['range'][0]}-{bin_data['range'][1]}",
                    "count": bin_data["count"],
                    "accurate": bin_data["accurate"],
                    "accuracy_rate": accuracy_pct
                }

        return result

    def _generate_recommendations(self, biases: list, strengths: dict, conviction_accuracy: dict) -> list:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Recommendations based on biases
        if biases:
            top_bias = biases[0]
            if top_bias['type'] == 'Sesgo de optimismo temporal':
                recommendations.append(
                    f"⚠️ Aumenta tus estimaciones de tiempo en 30-40%. "
                    f"Detectamos este sesgo en {top_bias['count']} decisiones."
                )
            elif top_bias['type'] == 'Infraestimación de riesgos':
                recommendations.append(
                    f"⚠️ Dedica más tiempo a análisis de riesgos. "
                    f"Este patrón aparece en {top_bias['count']} decisiones."
                )

        # Recommendations based on conviction accuracy
        if conviction_accuracy:
            high_conviction = conviction_accuracy.get('high', {})
            if high_conviction.get('accuracy_rate', 0) < 60:
                recommendations.append(
                    f"📊 Baja tu conviction en decisiones riesgosas. "
                    f"Cuando te sientes muy seguro (8-10), solo aciertas {high_conviction.get('accuracy_rate', 0)}%."
                )

        # Recommendations based on strengths
        if strengths and strengths.get('success_rate', 0) > 60:
            recommendations.append(
                f"✅ Mantén tu enfoque actual. Tienes {strengths.get('success_rate', 0)}% de éxito en decisiones completadas."
            )

        return recommendations

    def advise_decision(self, decision: dict, similar_decisions: list) -> dict:
        """
        Generate personalized decision advice based on similar past decisions.
        Analyzes patterns from similar decisions to provide actionable insights.
        """
        decision_id = decision.get('id')
        title = decision.get('title', 'tu decisión')
        decision_area = decision.get('area', '')
        decision_type = decision.get('decision_type', '')
        conviction = decision.get('conviction', 5)

        advisor_notes = []
        questions_to_consider = []

        if not similar_decisions:
            advisor_notes = [
                f"No hay suficientes decisiones similares completadas en el área de '{decision_area}' para generar un análisis comparativo.",
                "Completa más decisiones para que el sistema pueda aprender de patrones similares.",
            ]
            questions_to_consider = [
                "¿Qué supuestos clave estoy haciendo en esta decisión?",
                "¿Cuáles son los riesgos que podría estar subestimando?",
                "¿Qué evidencia contradice mi punto de vista actual?"
            ]
            return {
                "decision_id": decision_id,
                "title": title,
                "advisor_notes": advisor_notes,
                "questions_to_consider": questions_to_consider
            }

        # Analyze similar decisions
        advisor_notes.append(f"Basado en tu historial de {len(similar_decisions)} decisiones similares en {decision_area}:")

        # Check for timing delays
        delayed_count = sum(1 for d in similar_decisions if d.get('outcome_real') and
                           any(kw in d.get('outcome_real', '').lower() for kw in ["retraso", "delay", "tardó", "tarde"]))
        if delayed_count > 0:
            advisor_notes.append(
                f"- Tendencia a subestimar timeline: {delayed_count}/{len(similar_decisions)} decisiones fueron retrasadas"
            )
            questions_to_consider.append(
                "¿Cómo puedo añadir un buffer de tiempo del 30-50% a mi estimación actual?"
            )

        # Check conviction vs accuracy for similar decisions
        conviction_matches = [d for d in similar_decisions if d.get('conviction') and d.get('outcome_real')]
        if conviction_matches:
            avg_conviction = sum(d.get('conviction', 5) for d in conviction_matches) / len(conviction_matches)
            success_count = sum(1 for d in conviction_matches if any(
                kw in d.get('outcome_real', '').lower() for kw in ["acertado", "logrado", "éxito", "achieved", "bien"]
            ))
            accuracy_pct = (success_count / len(conviction_matches)) * 100 if conviction_matches else 0

            advisor_notes.append(
                f"- Tu conviction promedio en decisiones similares es {avg_conviction:.1f}/10 pero tu accuracy es {accuracy_pct:.0f}%"
            )

            if conviction > avg_conviction + 2 and accuracy_pct < 60:
                advisor_notes.append(
                    f"- ⚠️ Recomendación: Tu conviction actual ({conviction}/10) es más alta que el promedio. Considera ser más conservador."
                )
                questions_to_consider.append(
                    "¿Qué información nueva tengo que no había en decisiones anteriores similares?"
                )

        # Check for risk-related issues
        risk_issues = sum(1 for d in similar_decisions if d.get('outcome_real') and
                         any(kw in d.get('outcome_real', '').lower() for kw in ["riesgo", "problema", "issue", "complicación"]))
        if risk_issues > len(similar_decisions) * 0.4:
            advisor_notes.append(
                f"- Patrón detectado: Enfrentas complicaciones/riesgos inesperados en {risk_issues}/{len(similar_decisions)} casos"
            )
            questions_to_consider.append(
                "¿Qué riesgos he identificado? ¿Cuál es mi plan si cada uno ocurre?"
            )

        # Generic questions based on decision area
        if not questions_to_consider:
            questions_to_consider = [
                f"¿Cuáles son los supuestos clave en esta decisión de {decision_area}?",
                "¿Qué señales me indicarían que necesito cambiar de dirección?",
                "¿Cómo afectaría esta decisión a mis otras prioridades?"
            ]

        return {
            "decision_id": decision_id,
            "title": title,
            "advisor_notes": advisor_notes,
            "questions_to_consider": questions_to_consider
        }

    def detect_patterns(self, decisions: list, user_context: str) -> str:
        decisions_text = "\n".join([
            f"- {d['title']} ({d['area']}, {d.get('type', d.get('decision_type', 'unknown'))}): {d.get('status', 'sin resultado')}"
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
