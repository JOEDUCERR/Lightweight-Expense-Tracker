import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# Create a test database in memory.
# StaticPool + check_same_thread=False keeps a single in-memory connection
# shared across threads, which is required because FastAPI runs sync route
# handlers in a worker thread.
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create all tables in the test database
Base.metadata.create_all(bind=test_engine)

@pytest.fixture(scope="session")
def db():
    """Create a new database session for a test"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    """Create a test client for the FastAPI app"""
    # Override the database dependency to use the test database
    from app.database import get_db
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create TestClient properly (avoiding the app parameter issue)
    test_client = TestClient(app)
    yield test_client