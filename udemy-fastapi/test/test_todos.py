from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status
import pytest

app = __import__("app.03_restful_api.app", fromlist=["app"])
db = __import__("app.03_restful_api.db", fromlist=["db"])
users = __import__("app.03_restful_api.users", fromlist=["users"])
models = __import__("app.03_restful_api.models", fromlist=["models"])

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_user():
    return {
        "id": 1,
        "email": "john@example.com",
        "username": "john_doe",
        "is_superuser": False,
    }


app.app.dependency_overrides[db.get_db] = override_get_db
app.app.dependency_overrides[users.get_user] = override_get_user

client = TestClient(app.app)


@pytest.fixture
def test_todo():
    todo = models.Todo(
        title="Complete FastAPI tutorial",
        description="Go through the official FastAPI documentation",
        completed=True,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Welcome to Todo API with Authentication",
        "docs": "/docs",
        "version": "2.0.0",
    }
