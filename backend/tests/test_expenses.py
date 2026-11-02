import pytest
from app import models, schemas

# Global variables to store tokens and user info
test_user_token = None
test_user_id = None
test_expense_id = None

def test_create_expense(client):
    """Test creating an expense"""
    # First login to get token
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    global test_user_token, test_user_id
    test_user_token = response.json()["access_token"]
    
    # Create an expense
    response = client.post("/api/expenses", json={
        "title": "Grocery Shopping",
        "amount": 150.75,
        "description": "Weekly groceries"
    }, headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Grocery Shopping"
    assert data["amount"] == 150.75
    assert data["description"] == "Weekly groceries"
    global test_expense_id
    test_expense_id = data["id"]

def test_get_expenses(client):
    """Test retrieving all expenses"""
    response = client.get("/api/expenses", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    assert len(data["expenses"]) >= 1
    
    # Find our expense in the list
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None
    assert expense["title"] == "Grocery Shopping"

def test_get_expenses_with_filter_title(client):
    """Test retrieving expenses with title filter"""
    response = client.get("/api/expenses?title=Grocery", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    
    # Should find our expense
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None

def test_get_expenses_with_filter_min_amount(client):
    """Test retrieving expenses with minimum amount filter"""
    response = client.get("/api/expenses?min_amount=100", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    
    # Should find our expense
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None

def test_get_expenses_with_filter_max_amount(client):
    """Test retrieving expenses with maximum amount filter"""
    response = client.get("/api/expenses?max_amount=200", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    
    # Should find our expense
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None

def test_get_expenses_with_filter_description(client):
    """Test retrieving expenses with description filter"""
    response = client.get("/api/expenses?description=Weekly", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    
    # Should find our expense
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None

def test_get_expenses_with_combined_filters(client):
    """Test retrieving expenses with combined filters"""
    response = client.get("/api/expenses?title=Grocery&min_amount=100&max_amount=200", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    
    # Should find our expense
    expense = next((e for e in data["expenses"] if e["id"] == test_expense_id), None)
    assert expense is not None

def test_get_expenses_empty_results(client):
    """Test retrieving expenses with filters that return no results"""
    response = client.get("/api/expenses?title=NonExistent", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data
    assert "summary" in data
    assert len(data["expenses"]) == 0
    assert data["summary"]["total_count"] == 0
    assert data["summary"]["total_amount"] == 0.0
    assert data["summary"]["average_amount"] == 0.0

def test_get_expenses_summary(client):
    """Test that summary contains correct values"""
    response = client.get("/api/expenses", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check summary fields
    assert "summary" in data
    assert "total_count" in data["summary"]
    assert "total_amount" in data["summary"]
    assert "average_amount" in data["summary"]
    
    # Should have at least one expense
    assert data["summary"]["total_count"] >= 1
    assert data["summary"]["total_amount"] >= 0
    assert data["summary"]["average_amount"] >= 0

def test_get_single_expense(client):
    """Test retrieving a single expense"""
    response = client.get(f"/api/expenses/{test_expense_id}", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_expense_id
    assert data["title"] == "Grocery Shopping"

def test_update_expense(client):
    """Test updating an expense"""
    response = client.put(f"/api/expenses/{test_expense_id}", json={
        "title": "Grocery Shopping Updated",
        "amount": 200.00,
        "description": "Weekly groceries updated"
    }, headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_expense_id
    assert data["title"] == "Grocery Shopping Updated"
    assert data["amount"] == 200.00
    assert data["description"] == "Weekly groceries updated"

def test_delete_expense(client):
    """Test deleting an expense"""
    response = client.delete(f"/api/expenses/{test_expense_id}", headers={"Authorization": f"Bearer {test_user_token}"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Expense deleted successfully"}

def test_user_cannot_access_another_user_expense(client):
    """Test that a user cannot access another user's expenses"""
    # Register a second user
    response = client.post("/api/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    
    # Login as second user
    response = client.post("/api/auth/login", json={
        "username": "testuser2",
        "password": "password123"
    })
    
    token2 = response.json()["access_token"]

    # Try to access the first user's expense (should fail)
    response = client.get(f"/api/expenses/{test_expense_id}", headers={"Authorization": f"Bearer {token2}"})

    assert response.status_code == 404

def test_create_expense_invalid_amount(client):
    """Zero and negative amounts must be rejected with a validation error"""
    # Login to get token (testuser was created by test_auth.py earlier in the run)
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for bad_amount in (0, -25.5):
        response = client.post("/api/expenses/", json={
            "title": "Bad amount",
            "amount": bad_amount,
        }, headers=headers)
        assert response.status_code == 422, f"amount {bad_amount} should be rejected"
        assert response.json()["detail"][0]["loc"][-1] == "amount"

    # Unauthenticated creation must also be rejected
    response = client.post("/api/expenses/", json={
        "title": "No auth",
        "amount": 10.0,
    })
    assert response.status_code == 401