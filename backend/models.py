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


# Database setup
DATABASE_URL = "sqlite:///./cognitive_os.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
