from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123",
            "department": "Engineering",
            "designation": "Intern"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User registered successfully"


def test_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"