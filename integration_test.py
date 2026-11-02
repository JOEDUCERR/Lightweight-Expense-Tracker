#!/usr/bin/env python3

import requests
import time
from threading import Thread

def run_backend():
    """Start backend server in background"""
    import subprocess
    import os
    
    # Change to backend directory and start uvicorn
    backend_dir = "/home/techlead/Documents/Expense_Tracker/backend"
    
    # Start the backend with a different port to avoid conflicts
    cmd = ["uvicorn", "app.main:app", "--port", "8100", "--host", "0.0.0.0"]
    
    # Run in background
    process = subprocess.Popen(cmd, cwd=backend_dir)
    print("Backend started with PID:", process.pid)
    return process

def test_backend_endpoints():
    """Test backend endpoints directly"""
    
    print("\n=== Testing Backend Endpoints Directly ===")
    
    # Test health check
    try:
        response = requests.get('http://127.0.0.1:8100/health')
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test OpenAPI spec
    try:
        response = requests.get('http://127.0.0.1:8100/openapi.json')
        if response.status_code == 200:
            data = response.json()
            print("OpenAPI spec retrieved successfully")
            # Check if auth endpoints exist
            paths = list(data.get('paths', {}).keys())
            auth_endpoints = [p for p in paths if '/auth/' in p]
            print(f"Auth endpoints found: {auth_endpoints}")
        else:
            print(f"OpenAPI spec failed: {response.status_code}")
    except Exception as e:
        print(f"OpenAPI spec test failed: {e}")

def test_cors_preflight():
    """Test CORS preflight requests"""
    
    print("\n=== Testing CORS Preflight ===")
    
    # Test OPTIONS request to registration endpoint
    try:
        response = requests.options('http://127.0.0.1:8100/api/auth/register')
        print(f"OPTIONS /api/auth/register: {response.status_code}")
        if response.status_code == 200:
            print("✓ OPTIONS request successful")
        elif response.status_code == 405:
            print("✗ OPTIONS request failed with 405 - Method Not Allowed")
        else:
            print(f"? OPTIONS request returned: {response.status_code}")
    except Exception as e:
        print(f"OPTIONS test failed: {e}")

def main():
    print("Starting integration tests for Expense Tracker...")
    
    # Start backend
    backend_process = run_backend()
    
    # Give backend time to start
    time.sleep(3)
    
    try:
        # Test backend endpoints
        test_backend_endpoints()
        
        # Test CORS preflight 
        test_cors_preflight()
        
        print("\n=== Integration Test Complete ===")
        
    finally:
        # Clean up
        backend_process.terminate()
        backend_process.wait()

if __name__ == "__main__":
    main()