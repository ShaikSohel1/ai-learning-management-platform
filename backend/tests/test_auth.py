import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register():
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": test_email,
            "password": "password123",
            "department": "Engineering",
            "designation": "Intern"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"

    # Test duplicate email registration
    dup_response = client.post(
        "/auth/register",
        json={
            "name": "Test User 2",
            "email": test_email,
            "password": "password123",
            "department": "Engineering",
            "designation": "Intern"
        }
    )
    assert dup_response.status_code == 400
    assert dup_response.json()["detail"] == "Email already registered"


def test_login():
    test_email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    # Register user first
    client.post(
        "/auth/register",
        json={
            "name": "Login Test User",
            "email": test_email,
            "password": "password123",
            "department": "Engineering",
            "designation": "Developer"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": test_email,
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"