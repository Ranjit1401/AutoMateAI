"""Shared pytest fixtures: an isolated SQLite DB per test session and a
FastAPI TestClient wired to it, so tests never touch a real database or
require live API keys."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_automateai.db")
os.environ.setdefault("GROQ_API_KEY", "test-key-not-used-by-mocked-tests")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-" + "x" * 32)

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def _fresh_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def authed_client(client):
    client.post("/auth/signup", json={"email": "test@example.com", "password": "password123", "full_name": "Test User"})
    return client
