"""
AI Service for Cognitive OS - Analysis and reasoning
"""

import os
import json

# Try to import Claude SDK
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  Claude SDK not installed. Install with: pip install anthropic")


class AIAnalyzer:
    """Handles AI-powered analysis of decisions"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = "claude-opus-4-1"  # Modelo más reciente y estable
        self.client = anthropic.Anthropic(api_key=self.api_key) if CLAUDE_AVAILABLE and self.api_key else None

    def analyze_decision(self, decision: dict, user_context: str) -> str:
        """
        Analyze a decision for gaps, biases, and risks.
        """
        if not self.client:
            return self._demo_response("analyze", decision)

        prompt = f"""
{user_context}

DECISIÓN A ANALIZAR:
Título: {decision['title']}
Contexto: {decision['context']}
Tipo: {decision['decision_type']}
Área: {decision['area']}
Convicción: {decision.get('conviction', 'No especificada')}/10

Tu tarea como analista estratégico:
1. Identifica lagunas de información
2. Detecta sesgos cognitivos potenciales
3. Señala riesgos no considerados
4. Evalúa la calidad de la decisión
5. Propone preguntas incómodas

Sé directo y útil. No repitas lo que el usuario ya sabe.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en análisis: {str(e)}"

    def counterargument(self, decision: dict, user_context: str) -> str:
        """
        Challenge the decision with opposing viewpoints and worst-case scenarios.
        """
        if not self.client:
            return self._demo_response("counterargument", decision)

        prompt = f"""
{user_context}

DECISIÓN A CUESTIONAR:
Título: {decision['title']}
Contexto: {decision['context']}

Tu tarea como crítico riguroso:
Cuestiona explícitamente:
- Las premisas subyacentes
- Los supuestos ocultos
- El optimismo/pesimismo
- Las historias que se cuenta el usuario

Explora: ¿En qué escenarios falla esta decisión?
¿Qué señales se están ignorando?

Sé directo y provocador (en el buen sentido).
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en contraargumento: {str(e)}"

    def synthesize(self, decision: dict, analysis: str, counterargument: str) -> str:
        """
        Synthesize analysis and counterargument into clear summary.
        """
        if not self.client:
            return self._demo_response("synthesize", decision)

        prompt = f"""
DECISIÓN: {decision['title']}

ANÁLISIS:
{analysis}

CONTRAARGUMENTO:
{counterargument}

Tu tarea: Sintetiza en 3-4 puntos clave:
- Problema claro
- Opciones principales
- Trade-offs críticos
- Incertidumbre clave

Sin ruido. Directo al punto.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en síntesis: {str(e)}"

    def premortem(self, decision: dict, expected_outcome: str) -> str:
        """
        Pre-mortem: Imagine the decision fails, what went wrong?
        """
        if not self.client:
            return self._demo_response("premortem", decision)

        prompt = f"""
DECISIÓN: {decision['title']}
RESULTADO ESPERADO: {expected_outcome}

Imagina que en 6 meses esta decisión fracasa completamente.

Describe:
1. Qué salió mal específicamente
2. Por qué falló (causas raíz)
3. Qué señales se ignoraron
4. Cómo reconocerías el fallo temprano

Sé específico. Usa ejemplos concretos.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en pre-mortem: {str(e)}"

    def synthesize_decision(self, analysis: str, counterargument: str, premortem: str) -> str:
        """
        Synthesize all analyses into clear, actionable summary.
        """
        if not self.client:
            return self._demo_response("synthesize", {})

        prompt = f"""
ANÁLISIS COMPLETO DE UNA DECISIÓN:

ANÁLISIS:
{analysis}

CONTRAARGUMENTO:
{counterargument}

PRE-MORTEM:
{premortem}

Tu tarea: Sintetiza en máximo 5 puntos clave:
1. Problema claro (¿cuál es el verdadero problema?)
2. Opciones principales (¿qué alternativas reales hay?)
3. Trade-offs críticos (¿qué pierdo en cada opción?)
4. Incertidumbre clave (¿qué NO sé?)
5. Siguiente paso (¿qué hacer ahora?)

Sin ruido. Directo. Accionable.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en síntesis: {str(e)}"

    def review_decision(self, decision: dict, outcome: str, expected: str) -> str:
        """
        Review a decision: compare expectation vs reality.
        """
        if not self.client:
            return self._demo_response("review", decision)

        prompt = f"""
REVISIÓN DE DECISIÓN PASADA

DECISIÓN: {decision['title']}
CONTEXTO: {decision['context']}

RESULTADO ESPERADO:
{expected}

RESULTADO REAL:
{outcome}

Tu tarea:
1. Compara: ¿Qué funcionó? ¿Qué no?
2. Detecta: ¿Dónde fallaron los supuestos?
3. Analiza: ¿Qué señales se ignoraron?
4. Extrae: ¿Qué aprendiste?
5. Patrón: ¿Es un sesgo recurrente?

Sé específico. Usa números si es posible.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en revisión: {str(e)}"

    def detect_patterns(self, decisions: list, user_context: str) -> str:
        """
        Analyze multiple decisions to detect recurring patterns and biases.
        """
        if not self.client:
            return self._demo_response("patterns", {})

        decisions_text = "\n".join([
            f"- {d['title']} ({d['area']}, {d['decision_type']}): {d.get('status', 'sin resultado')}"
            for d in decisions[:10]  # Límitar a últimas 10 decisiones
        ])

        prompt = f"""
{user_context}

HISTORIAL DE DECISIONES:
{decisions_text}

Tu tarea como analista de patrones:
1. Detecta sesgos recurrentes (¿qué patrones ves?)
2. Identifica fortalezas (¿dónde aciertas?)
3. Señala puntos débiles (¿dónde fallas?)
4. Agrupa por tema (¿hay clusters?)
5. Sugiere mejora (¿qué cambiar?)

Sé constructivo. Baséate en datos (no intuición).
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error en patrones: {str(e)}"

    def _demo_response(self, analysis_type: str, decision: dict) -> str:
        """
        Demo responses when Claude API is not available.
        """
        demos = {
            "analyze": f"""[MODO DEMO - Claude API no disponible]

Análisis de: {decision['title']}

Lagunas identificadas:
- Falta contexto sobre competencia
- No hay datos sobre timeline
- Supuestos sobre recursos no validados

Sesgos detectados:
- Optimismo respecto a timeline
- Confirmación: buscando datos que apoyan la idea
- Disponibilidad: casos similares que salieron bien

Preguntas incómodas:
- ¿Qué pasa si el mercado cambia?
- ¿Cuánto te afecta si esto falla?
- ¿Qué estarías ignorando?

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "counterargument": f"""[MODO DEMO]

Escenarios donde {decision['title']} falla:

1. Mercado: El timing es incorrecto
2. Recursos: No hay suficiente budget
3. Equipo: Falta expertise crítica
4. Competencia: Alguien ya lo hizo mejor

Supuestos cuestionables:
- Asumir que X permanecerá estable
- Asumir que el equipo puede escalar

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "synthesize": """[MODO DEMO]

Síntesis:
- Problema: Decisión con fundamento pero riesgos no mitigados
- Opciones: A) Proceder con ajustes | B) Más análisis | C) Esperar señal
- Trade-offs: Rapidez vs seguridad
- Incertidumbre: Comportamiento del mercado

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "premortem": """[MODO DEMO]

Si esta decisión falla en 6 meses:

Causas raíz:
1. Estimaciones demasiado optimistas
2. Cambio en la prioridad del negocio
3. Falta de adopción de usuarios

Señales tempranas:
- Engagement bajo en primeros 2 meses
- Feedback negativo consistente
- Rotación de equipo clave

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "synthesize": """[MODO DEMO]

SÍNTESIS:

1. Problema claro
   La decisión tiene mérito pero riesgos no mitigados

2. Opciones principales
   A) Proceder con ajustes | B) Más análisis | C) Esperar señal

3. Trade-offs críticos
   Rapidez vs Seguridad | Control vs Delegación

4. Incertidumbre clave
   Comportamiento del mercado
   Capacidad de equipo
   Timeline real

5. Siguiente paso
   Definir 2-3 métricas clave para decidir rápido

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "review": """[MODO DEMO]

REVISIÓN:

Comparación: Expectativa vs Realidad
- Lo que funcionó: Ejecución fue más rápida
- Lo que no: Adopción fue más lenta

Sesgos ignorados:
- Supusiste que X, pero resultó Y
- Subvaloraste la curva de aprendizaje

Aprendizajes:
1. Necesitas más tiempo para validación
2. El mercado es más conservador
3. Comunidad es clave, no solo producto

Patrón recurrente:
Tendencia a ser optimista en timelines

Para análisis real, configura ANTHROPIC_API_KEY.""",

            "patterns": """[MODO DEMO]

PATRONES DETECTADOS:

Sesgos recurrentes:
- Optimismo en estimaciones (5 de 8 decisiones)
- Sobreestimar capacidad de equipo
- Subestimar fricción del mercado

Fortalezas:
✓ Análisis de competencia excelente
✓ Buena adaptabilidad a cambios
✓ Aprendes rápido de feedback

Puntos débiles:
✗ Planning financiero muy optimista
✗ No consultas a otros (sesgo de confirmación)
✗ Timing y recursos mal estimados

Mejoras sugeridas:
1. Multiplica timelines por 1.5x
2. Busca contraargumentos activamente
3. Valida supuestos con datos, no intuición

Para análisis real, configura ANTHROPIC_API_KEY."""
        }

        return demos.get(analysis_type, "Demo response")


# Initialize analyzer
analyzer = AIAnalyzer()


def get_analyzer():
    """Get or create AI analyzer instance"""
    return analyzer
