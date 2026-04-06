import logging
from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    google_id = Column(String, nullable=True, index=True)
    name = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)
    onboarded = Column(Integer, default=0)  # 0 = not onboarded, 1 = onboarded
    role = Column(String, nullable=True)
    decision_areas = Column(JSON, nullable=True)  # Array of strings
    decision_types = Column(JSON, nullable=True)  # Array of strings
    horizon = Column(String, nullable=True)
    known_bias = Column(String, nullable=True)
    decision_style = Column(String, nullable=True)  # "deliberativo", "intuitivo", "data-driven"
    risk_tolerance = Column(String, nullable=True)  # "conservador", "moderado", "agresivo"
    context_prompt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    context = Column(String)
    area = Column(String)  # One of the decision_areas
    decision_type = Column(String)  # "operational", "strategic", or "vital"
    options = Column(JSON)  # Array of decision options
    hypotheses = Column(JSON)  # Array of hypotheses
    signals = Column(JSON)  # Array of signals/data points
    conviction = Column(Integer, nullable=True)  # 1-10 scale
    decision_taken = Column(String, nullable=True)
    expected_outcome = Column(String, nullable=True)
    review_date = Column(String, nullable=True)  # ISO date string
    outcome_real = Column(String, nullable=True)
    learnings = Column(JSON, nullable=True)  # Array of learnings
    status = Column(String, default="draft")  # draft, analyzing, decided, reviewing, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, index=True)
    user_id = Column(String, index=True)
    analysis_type = Column(String)  # "analyze", "counterargument", "premortem", "synthesize-full", "patterns", etc.
    content = Column(String)  # Full analysis text
    analysis_data = Column(JSON, nullable=True)  # Additional data (e.g., key_findings, risks, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)


class Thought(Base):
    """
    Captures free-form thinking: ideas, observations, questions, reflections.
    Not just decisions - the entire cognitive process.
    """
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)  # Brief title/headline
    content = Column(String)  # Full thought content
    thought_type = Column(String)  # "idea", "observation", "question", "reflection", "hypothesis"
    area = Column(String, nullable=True)  # Related decision area (optional)
    tags = Column(JSON, nullable=True)  # Array of tags for organization
    status = Column(String, default="active")  # active, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Connection(Base):
    """
    Links thoughts and decisions together.
    Creates the memory structure: "This idea relates to..."
    """
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    source_type = Column(String)  # "thought" or "decision"
    source_id = Column(Integer)  # ID of the thought or decision
    target_type = Column(String)  # "thought" or "decision"
    target_id = Column(Integer)  # ID of the target thought or decision
    relationship = Column(String)  # "relates_to", "evolves_from", "contradicts", "supports", "questions"
    reason = Column(String, nullable=True)  # Why are they connected?
    created_at = Column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    """
    Temporal reminders to review decision outcomes.
    Closes the feedback loop by triggering outcome review at the right time.
    """
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    decision_id = Column(Integer, index=True)
    reminder_date = Column(DateTime, index=True)  # When to remind
    reminder_type = Column(String)  # "1month", "3months", "6months", "custom"
    message = Column(String, nullable=True)  # Custom reminder message
    status = Column(String, default="pending")  # pending, sent, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


class PublicLink(Base):
    """
    Public read-only links to share decisions.
    Enables viral sharing: others see value and create their own Cognitive OS.
    """
    __tablename__ = "public_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    decision_id = Column(Integer, index=True)
    token = Column(String, unique=True, index=True)  # Random token for URL
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration


class PersonalPattern(Base):
    """
    Personal decision-making patterns discovered during onboarding.
    Evolves as user makes more decisions.
    """
    __tablename__ = "personal_patterns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    pattern_type = Column(String)  # Type of pattern (e.g., "overconfidence", "external_attribution")
    title = Column(String)  # User-friendly title
    description = Column(String)  # Pattern description
    icon = Column(String)  # Emoji icon
    initial_strength = Column(Integer, default=5)  # How strong is this pattern (1-10)
    current_strength = Column(Integer, default=5)  # Updated based on new decisions
    examples = Column(JSON, nullable=True)  # Array of decision IDs that exemplify this pattern
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Database setup
DATABASE_URL = "sqlite:///./cognitive_os.db"

def init_db():
    """Initialize database with proper error handling and schema migration."""
    global engine, SessionLocal
    import os

    try:
        # Try main database first
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logging.info(f"✅ Database tables created successfully in {DATABASE_URL}")
        return True
    except Exception as db_error:
        # If it's a schema mismatch, try to reset the database
        if "no such column" in str(db_error):
            logging.warning(f"Schema mismatch detected: {db_error}")
            logging.info("   Resetting database to fix schema...")

            # Extract database filename from DATABASE_URL
            db_file = DATABASE_URL.replace("sqlite:///", "")
            if os.path.exists(db_file):
                os.remove(db_file)
                logging.info(f"   Deleted old database file: {db_file}")

            # Retry with fresh database
            try:
                engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
                Base.metadata.create_all(bind=engine)
                SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                logging.info(f"✅ Database reset and recreated successfully in {DATABASE_URL}")
                return True
            except Exception as retry_error:
                logging.error(f"Failed to recreate database: {retry_error}")
                raise

        logging.warning(f"Could not use main database: {db_error}")
        logging.info("   Falling back to temporary file-based database for this session")

        # Use a temporary file-based database instead of pure in-memory
        # This ensures the database is properly shared across connections
        try:
            import tempfile
            temp_db = tempfile.gettempdir() + "/cognitive_os_temp.db"
            fallback_url = f"sqlite:///{temp_db}"

            engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
            logging.info(f"✅ Temporary database initialized at {temp_db}")
            return True
        except Exception as fallback_error:
            logging.error(f"Failed to initialize fallback database: {fallback_error}")
            raise

# Initialize database on import
engine = None
SessionLocal = None
init_db()


def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
