import requests
import random
import string
import time
import sys
import json

BASE_URL = "https://backend01-mu.vercel.app/api"
HEALTH_URL = f"{BASE_URL}/health"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
TASKS_URL = f"{BASE_URL}/tasks"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_verification():
    session = requests.Session()
    
    print(f"Testing connectivity to {BASE_URL}...")
    
    # 1. Health Check
    try:
        print(f"1. Checking Health ({HEALTH_URL})...")
        response = session.get(HEALTH_URL, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code != 200:
            print("   [FAILED] Health check failed.")
            return False
    except Exception as e:
        print(f"   [FAILED] Exception during health check: {e}")
        return False

    # 2. Register
    email = f"test_{random_string(6)}@example.com"
    password = f"Pass{random_string(8)}!"
    full_name = f"Test User {random_string(4)}"
    
    print(f"\n2. Registering User ({email})...")
    payload = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    
    try:
        response = session.post(REGISTER_URL, json=payload, timeout=10)
        print(f"   Status Code: {response.status_code}")
        # print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   [SUCCESS] Registration successful.")
        else:
            print(f"   [FAILED] Registration failed. {response.text}")
            return False
    except Exception as e:
        print(f"   [FAILED] Exception during registration: {e}")
        return False

    # 3. Login (Note: Register usually logs you in via cookies, but let's test login explicitly or check cookies)
    # The register endpoint returns cookies. Let's see if we have them.
    cookies = session.cookies.get_dict()
    if 'access_token' in cookies:
        print("   [INFO] Registration returned access_token cookie.")
    else:
        print("   [INFO] No access_token cookie after registration. Attempting explicit login...")
        try:
            login_payload = {"email": email, "password": password}
            response = session.post(LOGIN_URL, json=login_payload, timeout=10)
            print(f"   Login Status Code: {response.status_code}")
            if response.status_code != 200:
                print(f"   [FAILED] Login failed. {response.text}")
                return False
            cookies = session.cookies.get_dict()
            if 'access_token' not in cookies:
                print("   [FAILED] Login successful but no access_token cookie received.")
                return False
            print("   [SUCCESS] Explicit login successful.")
        except Exception as e:
             print(f"   [FAILED] Exception during login: {e}")
             return False

    # 4. Create Task
    print(f"\n3. Creating Task...")
    task_payload = {
        "title": f"Test Task {random_string(5)}",
        "description": "This is a test task created by the verification script.",
        "priority": "medium",
        # "due_date": "2025-12-31T23:59:59Z" 
    }
    
    try:
        response = session.post(TASKS_URL, json=task_payload, timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 201:
            print("   [SUCCESS] Task created.")
            task_data = response.json()
            print(f"   Task ID: {task_data.get('id')}")
        else:
            print(f"   [FAILED] Task creation failed. {response.text}")
            return False
    except Exception as e:
        print(f"   [FAILED] Exception during task creation: {e}")
        return False

    # 5. List Tasks
    print(f"\n4. Listing Tasks...")
    try:
        response = session.get(TASKS_URL, timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            tasks_data = response.json()
            items = tasks_data.get('items', [])
            print(f"   [SUCCESS] Retrieved {len(items)} tasks.")
            # Verify our task is there
            # found = any(t['title'] == task_payload['title'] for t in items) # Might be paginated
            # if found:
            #     print("   [VERIFIED] Created task found in list.")
            # else:
            #     print("   [WARNING] Created task not found in first page of list.")
        else:
            print(f"   [FAILED] List tasks failed. {response.text}")
            return False
    except Exception as e:
        print(f"   [FAILED] Exception during listing tasks: {e}")
        return False
        
    print("\n[SUMMARY] Backend verification complete. All steps passed.")
    return True

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
