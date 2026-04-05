"""
Test Suite for Cognitive OS Backend
Tests cover: Authentication, Decisions, Outcomes, Patterns, Ideas, Connections
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

from main import app
from models import Base, User, Decision, Analysis, Thought, Connection, get_db, SessionLocal
from auth import create_jwt_token

# Create test database and session at module level
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_cognitive_os.db"
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create all tables
Base.metadata.create_all(bind=test_engine)

# Override get_db for all tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def clean_db():
    """Clean all data from test database"""
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f"DELETE FROM {table.name}"))
    db.commit()
    db.close()


# Clean before first test
clean_db()

# Create test client
@pytest.fixture
def client():
    """Create a TestClient with test database"""
    clean_db()
    return TestClient(app)

@pytest.fixture
def db_session():
    """Provide database session"""
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    # Clean up any existing test user first
    existing = db_session.query(User).filter(User.user_id == "test_user_123").first()
    if existing:
        db_session.delete(existing)
        db_session.commit()

    user = User(
        user_id="test_user_123",
        email="test@example.com",
        name="Test User",
        role="Product Manager",
        onboarded=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_header(test_user):
    """Generate JWT token for test user"""
    token = create_jwt_token(test_user.user_id, test_user.email)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_decision(test_user, db_session):
    """Create a test decision"""
    decision = Decision(
        user_id=test_user.user_id,
        title="Test Decision",
        context="Test context for decision",
        area="Product Strategy",
        decision_type="strategic",
        conviction=7,
        status="draft"
    )
    db_session.add(decision)
    db_session.commit()
    db_session.refresh(decision)
    return decision


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test authentication endpoints"""

    def test_test_login(self, client):
        """Test quick login endpoint"""
        response = client.post("/auth/test-login", json={"email": "testlogin@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user_id" in data
        assert data["onboarded"] == False

    def test_jwt_token_generation(self, test_user):
        """Test JWT token generation"""
        token = create_jwt_token(test_user.user_id, test_user.email)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0


# ============================================================================
# ONBOARDING TESTS
# ============================================================================

class TestOnboarding:
    """Test onboarding functionality"""

    def test_onboarding_flow(self, client, db_session):
        """Test complete onboarding flow"""
        # Create a non-onboarded user for this test
        new_user = User(
            user_id="onboarding_test_user",
            email="onboarding@example.com",
            name="Onboarding Test",
            onboarded=0
        )
        db_session.add(new_user)
        db_session.commit()

        # Create token for this user
        token = create_jwt_token(new_user.user_id, new_user.email)
        auth_header = {"Authorization": f"Bearer {token}"}

        onboarding_data = {
            "role": "Product Manager",
            "decision_areas": ["Product Strategy", "Team Management"],
            "decision_types": ["operational", "strategic"],
            "horizon": "quarterly",
            "known_bias": "Tend to overestimate capacity"
        }

        response = client.post(
            "/onboarding",
            json=onboarding_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["profile"]["user_id"] == new_user.user_id

    def test_onboarding_missing_fields(self, client, auth_header):
        """Test onboarding validation"""
        incomplete_data = {
            "role": "Product Manager"
            # Missing other required fields
        }

        response = client.post(
            "/onboarding",
            json=incomplete_data,
            headers=auth_header
        )

        # Should fail validation
        assert response.status_code != 200


# ============================================================================
# DECISION TESTS
# ============================================================================

class TestDecisions:
    """Test decision CRUD operations"""

    def test_create_decision(self, client, auth_header, test_user):
        """Test creating a new decision"""
        decision_data = {
            "title": "Expand to new market",
            "context": "We have capacity and budget",
            "area": "Product Strategy",
            "decision_type": "strategic",
            "conviction": 8
        }

        response = client.post(
            "/decisions",
            json=decision_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["decision_id"] is not None

    def test_get_decisions(self, client, auth_header, test_decision):
        """Test retrieving decisions"""
        response = client.get("/decisions", headers=auth_header)

        assert response.status_code == 200
        data = response.json()
        assert "decisions" in data
        assert len(data["decisions"]) > 0

    def test_get_single_decision(self, client, auth_header, test_decision):
        """Test retrieving a single decision"""
        response = client.get(
            f"/decisions/{test_decision.id}",
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_decision.title

    def test_update_decision(self, client, auth_header, test_decision):
        """Test updating a decision"""
        update_data = {
            "status": "analyzing",
            "decision_taken": "Chose Option A"
        }

        response = client.patch(
            f"/decisions/{test_decision.id}",
            json=update_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


# ============================================================================
# OUTCOMES TESTS
# ============================================================================

class TestOutcomes:
    """Test outcome registration and comparison"""

    def test_register_outcome(self, client, auth_header, test_decision, db_session):
        """Test registering an outcome"""
        test_decision.decision_taken = "Chose Option A"
        test_decision.expected_outcome = "30% growth"
        test_decision.status = "decided"

        db_session.merge(test_decision)
        db_session.commit()

        outcome_data = {
            "outcome_real": "15% growth achieved",
            "learnings": ["Underestimated market resistance", "Good timing"],
            "status": "completed"
        }

        response = client.post(
            f"/decisions/{test_decision.id}/outcome",
            json=outcome_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["outcome_real"] == "15% growth achieved"

    def test_get_outcome_comparison(self, client, auth_header, test_decision, db_session):
        """Test retrieving outcome comparison"""
        test_decision.expected_outcome = "30% growth"
        test_decision.outcome_real = "15% growth"
        test_decision.status = "completed"

        db_session.merge(test_decision)
        db_session.commit()

        response = client.get(
            f"/decisions/{test_decision.id}/outcome",
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["expected_outcome"] == "30% growth"
        assert data["outcome_real"] == "15% growth"


# ============================================================================
# IDEAS/THOUGHTS TESTS
# ============================================================================

class TestIdeas:
    """Test idea/thought capture"""

    def test_create_idea(self, client, auth_header, test_user):
        """Test creating an idea"""
        idea_data = {
            "title": "New feature concept",
            "content": "Users might benefit from...",
            "thought_type": "idea",
            "tags": ["product", "innovation"]
        }

        response = client.post(
            "/thoughts",
            json=idea_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["title"] == idea_data["title"]

    def test_list_ideas(self, client, auth_header, test_user):
        """Test retrieving ideas"""
        response = client.get("/thoughts", headers=auth_header)

        assert response.status_code == 200
        data = response.json()
        assert "thoughts" in data


# ============================================================================
# CONNECTIONS TESTS
# ============================================================================

class TestConnections:
    """Test idea and decision connections"""

    def test_create_connection(self, client, auth_header, test_decision):
        """Test creating a connection"""
        connection_data = {
            "source_type": "decision",
            "source_id": test_decision.id,
            "target_type": "decision",
            "target_id": test_decision.id,
            "relationship": "relates_to",
            "reason": "Both affect user retention"
        }

        response = client.post(
            "/connections",
            json=connection_data,
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "connected"


# ============================================================================
# AI ANALYSIS TESTS
# ============================================================================

class TestAIAnalysis:
    """Test AI-powered analysis features"""

    def test_analyze_decision(self, client, auth_header, test_decision):
        """Test decision analysis"""
        response = client.post(
            f"/decisions/{test_decision.id}/analyze",
            headers=auth_header
        )

        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert len(data["analysis"]) > 0

    def test_get_patterns(self, client, auth_header, test_user):
        """Test pattern detection"""
        response = client.get("/patterns", headers=auth_header)

        assert response.status_code == 200
        data = response.json()
        assert "total_decisions" in data
        assert "accuracy_rate" in data


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling and validation"""

    def test_unauthorized_access(self, client):
        """Test request without authentication"""
        response = client.get("/decisions")
        assert response.status_code == 401

    def test_invalid_decision_id(self, client, auth_header):
        """Test accessing non-existent decision"""
        response = client.get("/decisions/99999", headers=auth_header)
        assert response.status_code == 404

    def test_invalid_token(self, client):
        """Test request with invalid token"""
        response = client.get(
            "/decisions",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test complete workflows"""

    def test_complete_decision_workflow(self, client, auth_header, test_user):
        """Test complete decision workflow from creation to outcomes"""
        # 1. Create decision
        decision_data = {
            "title": "Launch new product",
            "context": "Market opportunity",
            "area": "Product Strategy",
            "decision_type": "strategic",
            "conviction": 7
        }
        response = client.post("/decisions", json=decision_data, headers=auth_header)
        assert response.status_code == 200
        decision_id = response.json()["decision_id"]

        # 2. Update with expected outcome
        update_data = {
            "status": "decided",
            "decision_taken": "Launch Q2 2024",
            "expected_outcome": "50% market adoption"
        }
        response = client.patch(f"/decisions/{decision_id}", json=update_data, headers=auth_header)
        assert response.status_code == 200

        # 3. Analyze decision
        response = client.post(f"/decisions/{decision_id}/analyze", headers=auth_header)
        assert response.status_code == 200

        # 4. Register outcome
        outcome_data = {
            "outcome_real": "25% adoption in first month",
            "learnings": ["Marketing was weak", "Product UX needs work"],
            "status": "completed"
        }
        response = client.post(f"/decisions/{decision_id}/outcome", json=outcome_data, headers=auth_header)
        assert response.status_code == 200

        # 5. Check patterns
        response = client.get("/patterns", headers=auth_header)
        assert response.status_code == 200


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test performance and scalability"""

    def test_bulk_decisions_loading(self, client, auth_header, test_user):
        """Test loading multiple decisions"""
        # Create 10 decisions
        for i in range(10):
            decision_data = {
                "title": f"Decision {i}",
                "context": f"Context {i}",
                "area": "Product Strategy",
                "decision_type": "operational"
            }
            client.post("/decisions", json=decision_data, headers=auth_header)

        # Load all decisions
        response = client.get("/decisions", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        assert len(data["decisions"]) == 10


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
