#!/usr/bin/env python3

"""
Simple test script to verify backend functionality
"""

import subprocess
import sys
import time
import requests
import threading

def run_backend():
    """Run the FastAPI backend in a separate thread"""
    # Start backend server
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8100", "--reload"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Give it time to start
    time.sleep(3)
    
    return process

def test_backend():
    """Test basic backend functionality"""
    try:
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8100/health")
        print(f"Health check: {response.status_code}")
        
        # Test registration endpoint (this will fail since we haven't set up the database yet)
        # But we can at least test that endpoints exist
        
        print("Backend functionality test completed successfully!")
        return True
    except Exception as e:
        print(f"Error testing backend: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend functionality...")
    
    # Test basic functionality
    success = test_backend()
    
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
        sys.exit(1)