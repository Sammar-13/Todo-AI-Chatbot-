import requests
import uuid
import sys
import json

# Configuration
BASE_URL = "https://full-stack-web-todo-app.vercel.app/api"
TIMEOUT = 30  # seconds

def log(message, type="INFO"):
    print(f"[{type}] {message}")

def verify_deployment():
    session = requests.Session()
    
    # Generate random user
    random_id = str(uuid.uuid4())[:8]
    email = f"deploy_test_{random_id}@example.com"
    password = "TestPassword123!"
    full_name = f"Test User {random_id}"

    log(f"Starting deployment verification for: {BASE_URL}")
    log(f"Test User: {email}")

    # 1. Test Health/Root
    try:
        log("Checking API health...")
        # Note: We are hitting the frontend proxy /api/health which rewrites to backend /api/health
        resp = session.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        log(f"Health check status: {resp.status_code}")
        if resp.status_code != 200:
            log(f"Health check failed: {resp.text}", "ERROR")
            # Continue anyway, sometimes health endpoints differ
    except Exception as e:
        log(f"Health check exception: {e}", "WARNING")

    # 2. Test Signup
    try:
        log("Attempting Signup...")
        signup_data = {
            "email": email,
            "password": password,
            "full_name": full_name
        }
        resp = session.post(f"{BASE_URL}/auth/register", json=signup_data, timeout=TIMEOUT)
        
        if resp.status_code != 201:
            log(f"Signup failed: {resp.status_code} - {resp.text}", "ERROR")
            return False
        
        log("Signup successful!")
        
        # Check cookies
        cookies = session.cookies.get_dict()
        if "access_token" in cookies:
            log("SUCCESS: 'access_token' cookie received!", "SUCCESS")
        else:
            log("WARNING: Signup succeeded but no 'access_token' cookie found. This might be okay if login is required separately, but typically register logs you in.", "WARNING")

    except Exception as e:
        log(f"Signup failed with exception: {e}", "ERROR")
        return False

    # 3. Test Login
    try:
        log("Attempting Login...")
        login_data = {
            "email": email,
            "password": password
        }
        # Clear cookies to force new login (optional, but good for testing)
        session.cookies.clear()
        
        resp = session.post(f"{BASE_URL}/auth/login", json=login_data, timeout=TIMEOUT)
        
        if resp.status_code != 200:
            log(f"Login failed: {resp.status_code} - {resp.text}", "ERROR")
            return False
            
        log("Login successful!")
        
        # Check cookies
        cookies = session.cookies.get_dict()
        if "access_token" in cookies:
            log("SUCCESS: 'access_token' cookie received via Vercel Proxy!", "SUCCESS")
        else:
            log("CRITICAL FAILURE: Login returned 200 OK but NO 'access_token' cookie was set. The Proxy/Cookie configuration is broken.", "ERROR")
            return False

    except Exception as e:
        log(f"Login failed with exception: {e}", "ERROR")
        return False

    # 4. Verify Session (GET /auth/verify)
    try:
        log("Verifying Session (GET /auth/verify)...")
        # The cookie is in the session, so it will be sent automatically
        resp = session.get(f"{BASE_URL}/auth/verify", timeout=TIMEOUT)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("authenticated") is True:
                log("SUCCESS: Session verified! User is authenticated.", "SUCCESS")
            else:
                log(f"Session verification returned 200 but authenticated=False: {data}", "ERROR")
                return False
        else:
            log(f"Session verification failed: {resp.status_code} - {resp.text}", "ERROR")
            return False

    except Exception as e:
        log(f"Session verification failed with exception: {e}", "ERROR")
        return False

    # 5. Create a Task (End-to-End Test)
    try:
        log("Attempting to create a task...")
        task_data = {
            "title": f"Test Task {random_id}",
            "description": "Created via automated deployment verification script",
            "priority": "high"
        }
        
        resp = session.post(f"{BASE_URL}/tasks", json=task_data, timeout=TIMEOUT)
        
        if resp.status_code in [200, 201]:
            log("SUCCESS: Task created successfully!", "SUCCESS")
            log(f"Task Response: {resp.json()}")
        else:
            log(f"Task creation failed: {resp.status_code} - {resp.text}", "ERROR")
            return False

    except Exception as e:
        log(f"Task creation failed with exception: {e}", "ERROR")
        return False

    log("-" * 50)
    log("DEPLOYMENT VERIFICATION COMPLETE: ALL SYSTEMS GO", "SUCCESS")
    return True

if __name__ == "__main__":
    success = verify_deployment()
    if not success:
        sys.exit(1)