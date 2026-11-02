import pytest
from app import schemas
from app.auth import get_password_hash


def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_username(client):
    """Test registering a user with duplicate username"""
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_register_duplicate_email(client):
    """Test registering a user with duplicate email"""
    response = client.post("/api/auth/register", json={
        "username": "testuser2",
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login(client):
    """Test user login"""
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    """Test login with wrong password"""
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "Incorrect email, username or password" in response.json()["detail"]

def test_login_with_email(client):
    """Test logging in using the registered email address"""
    response = client.post("/api/auth/login", json={
        "username": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_unauthenticated_access(client):
    """Test accessing protected endpoint without authentication"""
    response = client.get("/api/expenses")
    assert response.status_code == 401