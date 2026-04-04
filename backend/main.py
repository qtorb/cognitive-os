from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import json
import os

from models import User, Decision, get_db
from ai_service import get_analyzer
from auth import (
    create_jwt_token,
    verify_jwt_token,
    process_google_login,
    get_current_user
)

# Initialize FastAPI app
app = FastAPI(
    title="Cognitive OS",
    description="Personal cognitive operating system",
    version="0.1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# DEPENDENCY: Get current authenticated user
# ============================================================================

def get_token_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """
    Dependency to extract and verify JWT token from Authorization header.
    Returns the authenticated user.
    Expected format: "Bearer {token}"
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    # Parse "Bearer {token}"
    parts = authorization.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    token = parts[1]
    token_data = verify_jwt_token(token)
    user = db.query(User).filter(User.user_id == token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


# ============================================================================
# PYDANTIC MODELS (Request/Response schemas)
# ============================================================================

class OnboardingRequest(BaseModel):
    role: str
    decision_areas: list[str]
    decision_types: list[str]
    horizon: str
    known_bias: str | None = None


class UserProfile(BaseModel):
    user_id: str
    role: str
    decision_areas: list[str]
    decision_types: list[str]
    horizon: str
    known_bias: str | None
    context_prompt: str | None
    created_at: str

    class Config:
        from_attributes = True


class DecisionCreate(BaseModel):
    title: str
    context: str
    area: str
    decision_type: str
    options: list[str] = []
    hypotheses: list[str] = []
    signals: list[str] = []
    conviction: int | None = None


class DecisionUpdate(BaseModel):
    status: str | None = None
    decision_taken: str | None = None
    expected_outcome: str | None = None
    review_date: str | None = None
    outcome_real: str | None = None
    learnings: list[str] | None = None


class DecisionResponse(BaseModel):
    id: int
    user_id: str
    title: str
    context: str
    area: str
    decision_type: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


class GoogleAuthCallback(BaseModel):
    code: str


class AuthResponse(BaseModel):
    token: str
    user_id: str
    email: str
    name: str | None
    onboarded: bool


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_user_decision(decision_id: int, user: User, db: Session) -> Decision:
    """
    Get a decision and verify it belongs to the current user.
    """
    decision = db.query(Decision).filter(Decision.id == decision_id).first()

    if not decision:
        raise HTTPException(status_code=404, detail="Decisión no encontrada")

    if decision.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta decisión")

    return decision


def generate_context_prompt(user: User) -> str:
    """
    Generate a personalized AI context prompt based on user profile.
    This prompt will be used to personalize all AI analysis.
    """
    role = user.role
    areas = ", ".join(user.decision_areas)
    types = ", ".join(user.decision_types)
    horizon = user.horizon
    bias = user.known_bias or "no conocido"

    prompt = f"""Este usuario es: {role}

Toma decisiones en: {areas}

Tipos de decisión que considera importantes: {types}

Horizonte temporal: {horizon}

Sesgo reconocido: {bias}

En análisis y contraargumentación, personaliza según este contexto. Ayuda al usuario a pensar mejor dentro de sus áreas específicas de decisión."""

    return prompt


# ============================================================================
# ENDPOINTS: AUTHENTICATION
# ============================================================================

@app.get("/auth/login-url")
def get_google_login_url():
    """
    Return the Google OAuth login URL.
    Frontend should redirect user to this URL.
    """
    import os
    from urllib.parse import urlencode

    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback")

    params = {
        "client_id": google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline"
    }

    login_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    return {
        "login_url": login_url
    }


@app.post("/auth/callback")
def google_auth_callback(callback: GoogleAuthCallback, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Process Google OAuth callback.
    Frontend exchanges the authorization code for JWT token.
    """
    result = process_google_login(callback.code, db)

    return AuthResponse(**result)


@app.get("/auth/me")
def get_current_user_profile(user: User = Depends(get_token_user)) -> dict:
    """
    Get current authenticated user's profile.
    """
    return {
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "picture_url": user.picture_url,
        "onboarded": bool(user.onboarded),
        "role": user.role,
        "decision_areas": user.decision_areas,
        "decision_types": user.decision_types,
        "horizon": user.horizon,
        "known_bias": user.known_bias,
        "created_at": user.created_at.isoformat()
    }


# ============================================================================
# ENDPOINTS: ONBOARDING
# ============================================================================

@app.post("/onboarding")
def complete_onboarding(request: OnboardingRequest, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Complete user onboarding and create user profile.
    """
    # Check if already onboarded
    if user.onboarded:
        raise HTTPException(status_code=400, detail="Usuario ya completó el onboarding")

    # Generate context prompt
    temp_user = User(
        user_id=user.user_id,
        role=request.role,
        decision_areas=request.decision_areas,
        decision_types=request.decision_types,
        horizon=request.horizon,
        known_bias=request.known_bias,
        email=user.email
    )
    context_prompt = generate_context_prompt(temp_user)

    # Update user with onboarding data
    user.role = request.role
    user.decision_areas = request.decision_areas
    user.decision_types = request.decision_types
    user.horizon = request.horizon
    user.known_bias = request.known_bias
    user.context_prompt = context_prompt
    user.onboarded = 1

    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "message": "Perfil completado exitosamente",
        "profile": {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "decision_areas": user.decision_areas,
            "decision_types": user.decision_types,
            "horizon": user.horizon,
            "created_at": user.created_at.isoformat()
        }
    }


@app.get("/user/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Get user profile by ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "user_id": user.user_id,
        "role": user.role,
        "decision_areas": user.decision_areas,
        "decision_types": user.decision_types,
        "horizon": user.horizon,
        "known_bias": user.known_bias,
        "context_prompt": user.context_prompt,
        "created_at": user.created_at.isoformat()
    }


# ============================================================================
# ENDPOINTS: DECISIONS
# ============================================================================

@app.post("/decisions")
def create_decision(decision: DecisionCreate, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Create a new decision for the authenticated user.
    """
    # Verify user is onboarded
    if not user.onboarded:
        raise HTTPException(status_code=400, detail="Debes completar el onboarding primero")

    # Verify area is in user's decision areas
    if decision.area not in user.decision_areas:
        raise HTTPException(status_code=400, detail=f"El área '{decision.area}' no está en tus áreas de decisión")

    # Create decision
    new_decision = Decision(
        user_id=user.user_id,
        title=decision.title,
        context=decision.context,
        area=decision.area,
        decision_type=decision.decision_type,
        options=decision.options,
        hypotheses=decision.hypotheses,
        signals=decision.signals,
        conviction=decision.conviction,
        status="draft"
    )

    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    return {
        "status": "success",
        "decision_id": new_decision.id,
        "message": "Decisión registrada",
        "decision": {
            "id": new_decision.id,
            "title": new_decision.title,
            "area": new_decision.area,
            "status": new_decision.status,
            "created_at": new_decision.created_at.isoformat()
        }
    }


@app.get("/decisions")
def list_decisions(user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    List all decisions for the authenticated user.
    """
    decisions = db.query(Decision).filter(Decision.user_id == user.user_id).order_by(Decision.created_at.desc()).all()

    return {
        "user_id": user.user_id,
        "count": len(decisions),
        "decisions": [
            {
                "id": d.id,
                "title": d.title,
                "context": d.context,
                "area": d.area,
                "decision_type": d.decision_type,
                "status": d.status,
                "created_at": d.created_at.isoformat(),
                "conviction": d.conviction
            }
            for d in decisions
        ]
    }


@app.get("/decisions/{decision_id}")
def get_decision(decision_id: int, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Get a specific decision by ID.
    """
    decision = get_user_decision(decision_id, user, db)

    return {
        "id": decision.id,
        "user_id": decision.user_id,
        "title": decision.title,
        "context": decision.context,
        "area": decision.area,
        "decision_type": decision.decision_type,
        "options": decision.options,
        "hypotheses": decision.hypotheses,
        "signals": decision.signals,
        "conviction": decision.conviction,
        "status": decision.status,
        "decision_taken": decision.decision_taken,
        "expected_outcome": decision.expected_outcome,
        "review_date": decision.review_date,
        "outcome_real": decision.outcome_real,
        "learnings": decision.learnings,
        "created_at": decision.created_at.isoformat(),
        "updated_at": decision.updated_at.isoformat()
    }


@app.patch("/decisions/{decision_id}")
def update_decision(decision_id: int, update: DecisionUpdate, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Update a decision.
    """
    decision = get_user_decision(decision_id, user, db)

    # Update fields if provided
    if update.status:
        decision.status = update.status
    if update.decision_taken:
        decision.decision_taken = update.decision_taken
    if update.expected_outcome:
        decision.expected_outcome = update.expected_outcome
    if update.review_date:
        decision.review_date = update.review_date
    if update.outcome_real:
        decision.outcome_real = update.outcome_real
    if update.learnings:
        decision.learnings = update.learnings

    decision.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(decision)

    return {
        "status": "success",
        "message": "Decisión actualizada",
        "decision_id": decision.id
    }


# ============================================================================
# ENDPOINTS: AI ANALYSIS
# ============================================================================

@app.post("/decisions/{decision_id}/analyze")
def analyze_decision(decision_id: int, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Analyze a decision using AI.
    Identifies gaps, biases, and risks.
    """
    decision = get_user_decision(decision_id, user, db)

    analyzer = get_analyzer()
    analysis = analyzer.analyze_decision(
        {
            "title": decision.title,
            "context": decision.context,
            "decision_type": decision.decision_type,
            "area": decision.area,
            "conviction": decision.conviction
        },
        user.context_prompt
    )

    return {
        "decision_id": decision_id,
        "analysis_type": "analyze",
        "analysis": analysis
    }


@app.post("/decisions/{decision_id}/counterargument")
def counterargument_decision(decision_id: int, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Challenge a decision with opposing viewpoints.
    """
    decision = get_user_decision(decision_id, user, db)

    analyzer = get_analyzer()
    counterargument = analyzer.counterargument(
        {
            "title": decision.title,
            "context": decision.context,
            "decision_type": decision.decision_type,
            "area": decision.area
        },
        user.context_prompt
    )

    return {
        "decision_id": decision_id,
        "analysis_type": "counterargument",
        "analysis": counterargument
    }


@app.post("/decisions/{decision_id}/synthesize")
def synthesize_decision(
    decision_id: int,
    analysis: str,
    counterargument: str,
    user: User = Depends(get_token_user),
    db: Session = Depends(get_db)
):
    """
    Synthesize analysis and counterargument.
    """
    decision = get_user_decision(decision_id, user, db)

    analyzer = get_analyzer()
    synthesis = analyzer.synthesize(
        {
            "title": decision.title,
            "context": decision.context
        },
        analysis,
        counterargument
    )

    return {
        "decision_id": decision_id,
        "analysis_type": "synthesize",
        "analysis": synthesis
    }


@app.post("/decisions/{decision_id}/premortem")
def premortem_decision(decision_id: int, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Pre-mortem: Imagine the decision fails.
    """
    decision = get_user_decision(decision_id, user, db)

    expected_outcome = decision.expected_outcome or "éxito en la implementación"

    analyzer = get_analyzer()
    premortem = analyzer.premortem(
        {
            "title": decision.title,
            "context": decision.context
        },
        expected_outcome
    )

    return {
        "decision_id": decision_id,
        "analysis_type": "premortem",
        "analysis": premortem
    }


@app.post("/decisions/{decision_id}/synthesize-full")
def synthesize_full_decision(decision_id: int, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Full synthesis: Integrate all analyses into clear summary.
    Requires running analyze, counterargument, and premortem first.
    """
    decision = get_user_decision(decision_id, user, db)

    analyzer = get_analyzer()

    # Run all analyses
    decision_data = {
        "title": decision.title,
        "context": decision.context,
        "decision_type": decision.decision_type,
        "area": decision.area,
        "conviction": decision.conviction
    }

    analysis = analyzer.analyze_decision(decision_data, user.context_prompt)
    counterargument = analyzer.counterargument(decision_data, user.context_prompt)
    premortem = analyzer.premortem(decision_data, decision.expected_outcome or "éxito")

    synthesis = analyzer.synthesize_decision(analysis, counterargument, premortem)

    return {
        "decision_id": decision_id,
        "analysis_type": "synthesize",
        "analysis": synthesis
    }


@app.post("/decisions/{decision_id}/review")
def review_decision(decision_id: int, outcome_real: str, user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Review a completed decision: compare expectation vs reality.
    """
    decision = get_user_decision(decision_id, user, db)

    analyzer = get_analyzer()
    review = analyzer.review_decision(
        {
            "title": decision.title,
            "context": decision.context
        },
        outcome_real,
        decision.expected_outcome or "no especificado"
    )

    return {
        "decision_id": decision_id,
        "analysis_type": "review",
        "analysis": review
    }


@app.get("/patterns")
def analyze_patterns(user: User = Depends(get_token_user), db: Session = Depends(get_db)):
    """
    Analyze patterns across all user's decisions.
    Detects recurring biases and strengths.
    """

    decisions = db.query(Decision).filter(Decision.user_id == user.user_id).order_by(Decision.created_at.desc()).limit(10).all()

    if not decisions:
        return {
            "user_id": user.user_id,
            "analysis_type": "patterns",
            "analysis": "No hay suficientes decisiones registradas para detectar patrones. Registra al menos 3-5 decisiones."
        }

    decisions_data = [
        {
            "title": d.title,
            "area": d.area,
            "decision_type": d.decision_type,
            "status": d.status,
            "context": d.context
        }
        for d in decisions
    ]

    analyzer = get_analyzer()
    patterns = analyzer.detect_patterns(decisions_data, user.context_prompt)

    return {
        "user_id": user.user_id,
        "decision_count": len(decisions),
        "analysis_type": "patterns",
        "analysis": patterns
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "service": "Cognitive OS API"}


# ============================================================================
# STATIC FILES (mounted LAST so API endpoints take priority)
# ============================================================================

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=parent_dir, html=True), name="static")


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
