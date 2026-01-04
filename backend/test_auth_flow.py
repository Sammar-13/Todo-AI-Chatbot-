"""
Automated tests for HTTP-only cookie authentication flow
Tests the complete user journey: signup -> create task -> refresh -> logout -> login
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import httpx
from app.config import settings

# Test configuration
API_URL = "http://localhost:8000/api"
TEST_EMAIL = "autotest@example.com"
TEST_PASSWORD = "AutoTest123!"
TEST_NAME = "Auto Test User"

# Test results
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def log_test(name: str, passed: bool, message: str = ""):
    """Log test result"""
    results["total"] += 1
    if passed:
        results["passed"] += 1
        status = "[PASS]"
    else:
        results["failed"] += 1
        status = "[FAIL]"

    results["tests"].append({
        "name": name,
        "passed": passed,
        "message": message
    })

    print(f"{status}: {name}")
    if message:
        print(f"     {message}")

async def test_signup():
    """Test 1: User signup and account creation"""
    print("\n" + "="*80)
    print("TEST 1: SIGNUP (Create account with HTTP-only cookies)")
    print("="*80)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/auth/register",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD,
                    "full_name": TEST_NAME
                }
            )

            # Check status code
            if response.status_code != 201:
                log_test("Signup request", False, f"Expected 201, got {response.status_code}")
                return None
            log_test("Signup request", True, "Status: 201 Created")

            # Check response has user data
            data = response.json()
            if "user" not in data:
                log_test("User data in response", False, "No user in response")
                return None
            log_test("User data in response", True, f"Email: {data['user']['email']}")

            # Check cookies are set
            cookies = response.cookies
            if "access_token" not in cookies:
                log_test("Access token cookie", False, "No access_token cookie")
                return None
            log_test("Access token cookie", True, "Cookie set")

            if "refresh_token" not in cookies:
                log_test("Refresh token cookie", False, "No refresh_token cookie")
                return None
            log_test("Refresh token cookie", True, "Cookie set")

            # Check cookies have correct flags
            set_cookie_header = response.headers.get("set-cookie", "")
            if "HttpOnly" in set_cookie_header:
                log_test("HttpOnly flag", True, "Cookies are HttpOnly")
            else:
                log_test("HttpOnly flag", False, "HttpOnly flag not set")

            return cookies

    except Exception as e:
        import traceback
        traceback.print_exc()
        log_test("Signup test", False, str(e))
        return None

async def test_create_task(cookies):
    """Test 2: Create task while authenticated"""
    print("\n" + "="*80)
    print("TEST 2: CREATE TASK (With authentication cookies)")
    print("="*80)

    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.post(
                f"{API_URL}/tasks",
                json={
                    "title": "Buy groceries",
                    "description": "Test task for automated testing",
                    "priority": "medium"
                }
            )

            if response.status_code != 201:
                log_test("Create task request", False, f"Expected 201, got {response.status_code}")
                return None
            log_test("Create task request", True, "Status: 201 Created")

            data = response.json()
            if "id" not in data:
                log_test("Task ID in response", False, "No task ID")
                return None
            log_test("Task ID in response", True, f"Task ID: {data['id']}")

            if data.get("title") != "Buy groceries":
                log_test("Task title", False, "Title mismatch")
                return None
            log_test("Task title", True, f"Title: {data['title']}")

            # Check Cookie header was sent
            print(f"     Request had cookies: {'access_token' in str(cookies)}")

            return data

    except Exception as e:
        log_test("Create task test", False, str(e))
        return None

async def test_verify_session(cookies):
    """Test 3: Verify session (simulates page refresh)"""
    print("\n" + "="*80)
    print("TEST 3: VERIFY SESSION (Simulates page refresh - GET /auth/verify)")
    print("="*80)

    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.get(f"{API_URL}/auth/verify")

            if response.status_code != 200:
                log_test("Verify session request", False, f"Expected 200, got {response.status_code}")
                return False
            log_test("Verify session request", True, "Status: 200 OK")

            data = response.json()
            if not data.get("authenticated"):
                log_test("Session authenticated", False, "Not authenticated")
                return False
            log_test("Session authenticated", True, "User is authenticated")

            if "user" not in data:
                log_test("User in verify response", False, "No user data")
                return False
            log_test("User in verify response", True, f"Email: {data['user']['email']}")

            return True

    except Exception as e:
        log_test("Verify session test", False, str(e))
        return False

async def test_get_tasks(cookies):
    """Test 4: Get tasks (verify data persists after refresh)"""
    print("\n" + "="*80)
    print("TEST 4: GET TASKS (Verify task persisted)")
    print("="*80)

    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.get(f"{API_URL}/tasks")

            if response.status_code != 200:
                log_test("Get tasks request", False, f"Expected 200, got {response.status_code}")
                return False
            log_test("Get tasks request", True, "Status: 200 OK")

            data = response.json()
            # Check for paginated response structure
            if "items" not in data:
                log_test("Tasks format", False, "Expected 'items' in response (paginated)")
                return False
            
            tasks = data["items"]
            if not isinstance(tasks, list):
                log_test("Tasks list format", False, "Expected list in 'items'")
                return False
            log_test("Tasks format", True, f"Got {len(tasks)} task(s)")

            # Check first task
            if len(tasks) > 0 and tasks[0].get("title") == "Buy groceries":
                log_test("Task data persisted", True, f"Task found: {tasks[0]['title']}")
                return True
            else:
                log_test("Task data persisted", False, "Expected task not found")
                return False

    except Exception as e:
        log_test("Get tasks test", False, str(e))
        return False

async def test_create_second_task(cookies):
    """Test 5: Create second task (verify continued functionality after refresh)"""
    print("\n" + "="*80)
    print("TEST 5: CREATE SECOND TASK (After session verification)")
    print("="*80)

    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.post(
                f"{API_URL}/tasks",
                json={
                    "title": "Pay bills",
                    "description": "Test second task",
                    "priority": "high"
                }
            )

            if response.status_code != 201:
                log_test("Create second task", False, f"Expected 201, got {response.status_code}")
                return False
            log_test("Create second task", True, "Status: 201 Created")

            data = response.json()
            if data.get("title") == "Pay bills":
                log_test("Second task data", True, f"Title: {data['title']}")
                return True
            else:
                log_test("Second task data", False, "Title mismatch")
                return False

    except Exception as e:
        log_test("Create second task test", False, str(e))
        return False

async def test_logout(cookies):
    """Test 6: Logout and verify cookies are cleared"""
    print("\n" + "="*80)
    print("TEST 6: LOGOUT (Clear cookies)")
    print("="*80)

    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.post(f"{API_URL}/auth/logout")

            if response.status_code != 200:
                log_test("Logout request", False, f"Expected 200, got {response.status_code}")
                return False
            log_test("Logout request", True, "Status: 200 OK")

            # Check response message
            data = response.json()
            if "Successfully logged out" in data.get("message", ""):
                log_test("Logout message", True, f"Message: {data['message']}")
                return True
            else:
                log_test("Logout message", False, "Unexpected response")
                return False

    except Exception as e:
        log_test("Logout test", False, str(e))
        return False

async def test_login_again():
    """Test 7: Login with same credentials and verify tasks are still there"""
    print("\n" + "="*80)
    print("TEST 7: LOGIN AGAIN (Verify task persistence from database)")
    print("="*80)

    try:
        async with httpx.AsyncClient() as client:
            # Login
            response = await client.post(
                f"{API_URL}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )

            if response.status_code != 200:
                log_test("Login request", False, f"Expected 200, got {response.status_code}")
                return False
            log_test("Login request", True, "Status: 200 OK")

            cookies = response.cookies

            # Get tasks with new session
            async with httpx.AsyncClient(cookies=cookies) as authenticated_client:
                tasks_response = await authenticated_client.get(f"{API_URL}/tasks")

                if tasks_response.status_code != 200:
                    log_test("Get tasks after login", False, f"Expected 200, got {tasks_response.status_code}")
                    return False

                data = tasks_response.json()
                if "items" not in data:
                    log_test("Get tasks after login", False, "Response missing 'items' field")
                    return False
                
                tasks = data["items"]
                if len(tasks) >= 2:
                    log_test("Get tasks after login", True, f"Got {len(tasks)} tasks")

                    # Check for both tasks
                    task_titles = [t.get("title") for t in tasks]
                    if "Buy groceries" in task_titles:
                        log_test("First task persisted", True, "Found: Buy groceries")
                    else:
                        log_test("First task persisted", False, "Buy groceries not found")

                    if "Pay bills" in task_titles:
                        log_test("Second task persisted", True, "Found: Pay bills")
                        return True
                    else:
                        log_test("Second task persisted", False, "Pay bills not found")
                        return False
                else:
                    log_test("Get tasks after login", False, f"Expected 2+ tasks, got {len(tasks)}")
                    return False

    except Exception as e:
        log_test("Login again test", False, str(e))
        return False

async def test_verify_endpoint_behavior():
    """Test 8: Verify endpoint returns unauthenticated when no cookies"""
    print("\n" + "="*80)
    print("TEST 8: VERIFY ENDPOINT (No cookies = unauthenticated)")
    print("="*80)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/auth/verify")

            if response.status_code != 200:
                log_test("Verify without cookies", False, f"Expected 200, got {response.status_code}")
                return False
            log_test("Verify without cookies", True, "Status: 200 OK")

            data = response.json()
            if not data.get("authenticated"):
                log_test("Unauthenticated response", True, "Correctly returns unauthenticated")
                return True
            else:
                log_test("Unauthenticated response", False, "Should be unauthenticated")
                return False

    except Exception as e:
        log_test("Verify endpoint test", False, str(e))
        return False

async def run_all_tests():
    """Run complete test suite"""
    print("\n")
    print("=" * 80)
    print("HTTP-Only Cookie Authentication - Automated Test Suite".center(80))
    print("=" * 80)

    # Test 1: Signup
    cookies = await test_signup()
    if not cookies:
        log_test("Test flow", False, "Signup failed, cannot continue")
        return

    # Test 2: Create task
    task = await test_create_task(cookies)
    if not task:
        log_test("Test flow", False, "Task creation failed, cannot continue")

    # Test 3: Verify session (page refresh simulation)
    verified = await test_verify_session(cookies)
    if not verified:
        log_test("Test flow", False, "Session verification failed")

    # Test 4: Get tasks (verify persistence)
    await test_get_tasks(cookies)

    # Test 5: Create second task
    await test_create_second_task(cookies)

    # Test 6: Logout
    await test_logout(cookies)

    # Test 7: Login again
    await test_login_again()

    # Test 8: Verify endpoint behavior
    await test_verify_endpoint_behavior()

    # Print results summary
    print("\n")
    print("=" * 80)
    print("TEST RESULTS SUMMARY".center(80))
    print("=" * 80)
    print(f"\nTotal Tests:  {results['total']}")
    print(f"Passed:       {results['passed']} [OK]")
    print(f"Failed:       {results['failed']} [FAILED]")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")

    if results['failed'] == 0:
        print("\n[SUCCESS] ALL TESTS PASSED! HTTP-only cookie authentication is working!")
        return 0
    else:
        print(f"\n[WARNING] {results['failed']} test(s) failed. Review errors above.")
        return 1

# Run tests
if __name__ == "__main__":
    try:
        exit_code = asyncio.run(run_all_tests())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[WARNING] Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Fatal error: {e}")
        sys.exit(1)
