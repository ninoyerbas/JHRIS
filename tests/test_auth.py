"""
Tests for authentication endpoints.
"""
import pytest
from app.config import settings


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json={"email": "newuser@example.com", "password": "newpassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert data["is_active"] is True
    assert data["is_superuser"] is False


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json={"email": test_user.email, "password": "anypassword"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login(client, test_user):
    """Test user login."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={"username": test_user.email, "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={"username": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user info."""
    response = client.get(
        f"{settings.API_V1_PREFIX}/auth/me",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_refresh_token(client, auth_headers):
    """Test token refresh."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/refresh",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
