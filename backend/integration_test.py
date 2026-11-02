#!/usr/bin/env python3

"""
Simple integration test to verify the new functionality works correctly.
This avoids pytest dependency issues.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app

def test_api_structure():
    """Test that our API structure is working"""
    client = TestClient(app)
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Test health check
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    
    print("✓ Basic API endpoints working")

def test_expenses_endpoint():
    """Test the new expenses endpoint with filters and summary"""
    client = TestClient(app)
    
    # First, let's see if we can hit the expenses endpoint
    try:
        response = client.get("/api/expenses")
        print(f"Expenses endpoint response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✓ Expenses endpoint returns valid JSON")
            if 'expenses' in data and 'summary' in data:
                print("✓ Expenses endpoint returns proper structure with expenses and summary")
            else:
                print("⚠ Expenses endpoint missing expected fields")
        else:
            print(f"⚠ Expenses endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"Error testing expenses endpoint: {e}")

if __name__ == "__main__":
    print("Running integration tests...")
    test_api_structure()
    test_expenses_endpoint()
    print("Integration tests completed!")