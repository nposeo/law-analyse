"""Test suite for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.database import Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    """Test root endpoint returns health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_create_law():
    """Test creating a law."""
    law_data = {
        "title": "Тестовий закон",
        "document_number": "1234-IX",
        "issuing_body": "Верховна Рада України"
    }

    response = client.post("/laws/", json=law_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовий закон"
    assert data["document_number"] == "1234-IX"
    assert "id" in data


def test_get_all_laws():
    """Test getting all laws."""
    # Create a law first
    law_data = {"title": "Закон 1"}
    client.post("/laws/", json=law_data)

    response = client.get("/laws/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_law_by_id():
    """Test getting law by ID."""
    # Create a law
    law_data = {"title": "Закон для тесту"}
    create_response = client.post("/laws/", json=law_data)
    law_id = create_response.json()["id"]

    # Get the law
    response = client.get(f"/laws/{law_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Закон для тесту"


def test_get_nonexistent_law():
    """Test getting non-existent law returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/laws/{fake_id}")
    assert response.status_code == 404


@pytest.mark.skip(reason="Requires file upload setup")
def test_upload_pdf():
    """Test PDF upload endpoint."""
    # This would require actual file upload testing
    pass


def test_get_articles_for_nonexistent_law():
    """Test getting articles for non-existent law."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/articles/law/{fake_id}")
    assert response.status_code == 404


def test_processing_status_for_nonexistent_law():
    """Test processing status for non-existent law."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/process/{fake_id}/status")
    assert response.status_code == 404
