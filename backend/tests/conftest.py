import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import settings
from app.db.session import Base, get_db
from app.main import app

DATABASE_TEST_URL = settings.DATABASE_TEST_URL

engine = create_engine(DATABASE_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ----------------------------------------
# Create test database schema once per session
# ----------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ----------------------------------------
# Provide a transactional database session per test
# ----------------------------------------
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ----------------------------------------
# Override the global get_db dependency
# ----------------------------------------
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.pop(get_db, None)


# ----------------------------------------
# FastAPI TestClient
# ----------------------------------------
@pytest.fixture
def client():
    return TestClient(app)


# ----------------------------------------
# Create a test user with known credentials
# ----------------------------------------
@pytest.fixture
def test_user(db_session):
    from app.core.security import hash_password

    password = "testpass123"
    username = "testuser"
    hashed = hash_password(password)

    result = db_session.execute(
        text(
            """
            INSERT INTO users (username, password_hash)
            VALUES (:username, :hash)
            RETURNING user_id
            """
        ),
        {"username": username, "hash": hashed},
    )
    user_id = result.scalar_one()

    db_session.commit()
    return {"user_id": user_id, "username": username, "password": password}


# ----------------------------------------
# Obtain an authentication token for the test user
# ----------------------------------------
@pytest.fixture
def auth_token(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == 200, "Login failed"
    return response.json()["access_token"]
