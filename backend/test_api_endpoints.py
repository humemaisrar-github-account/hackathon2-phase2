import requests
import json
import uuid
from sqlmodel import Session
from src.database.database import engine
from src.models.user import User
from src.services.user_service import UserService


def test_api_endpoints():
    """
    Test the API endpoints directly to ensure JWT authentication works properly
    """
    print("Testing API endpoints with JWT authentication...")

    # Create a test user in the database
    with Session(engine) as session:
        test_email = f"api_test_{uuid.uuid4()}@example.com"
        test_password = "testpassword123"

        print(f"Creating test user with email: {test_email}")
        user = UserService.create_user(session, test_email, test_password)
        user_id = user.id
        print(f"Created user with ID: {user_id}")

    # Start the FastAPI app in a subprocess to test the endpoints
    import subprocess
    import time
    import signal
    import os

    # Start the server in the background
    print("Starting server...")
    proc = subprocess.Popen(["python", "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "warning"])

    # Give the server time to start
    time.sleep(3)

    try:
        # Test the server is running
        response = requests.get("http://127.0.0.1:8000/")
        assert response.status_code == 200
        print("✓ Server is running")

        # Test login to get JWT token
        login_response = requests.post("http://127.0.0.1:8000/api/auth/login",
                                    json={"email": test_email, "password": test_password})
        print(f"Login response: {login_response.status_code}")
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        jwt_token = login_data["access_token"]
        print("✓ Got JWT token")

        # Test getting token via email (for when user is authenticated via BetterAuth)
        token_response = requests.post("http://127.0.0.1:8000/api/auth/token",
                                    json={"email": test_email})
        print(f"Token response: {token_response.status_code}")
        assert token_response.status_code == 200
        token_data = token_response.json()
        assert "access_token" in token_data
        jwt_token = token_data["access_token"]
        print("✓ Got JWT token via email")

        # Test GET /api/{user_id}/tasks with proper authentication
        headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
        get_response = requests.get(f"http://127.0.0.1:8000/api/{user_id}/tasks", headers=headers)
        print(f"GET /api/{user_id}/tasks response: {get_response.status_code}")
        if get_response.status_code == 200:
            print("✓ GET /api/{user_id}/tasks successful")
        elif get_response.status_code == 403:
            print("✗ GET /api/{user_id}/tasks failed with 403 - user ID mismatch")
            print(f"Response: {get_response.text}")
        else:
            print(f"✗ Unexpected response: {get_response.status_code} - {get_response.text}")

        # Test POST /api/{user_id}/tasks with proper authentication
        post_response = requests.post(f"http://127.0.0.1:8000/api/{user_id}/tasks",
                                   json={"title": "API Test Todo", "description": "Test from API", "is_completed": False},
                                   headers=headers)
        print(f"POST /api/{user_id}/tasks response: {post_response.status_code}")
        if post_response.status_code == 201 or post_response.status_code == 200:
            print("✓ POST /api/{user_id}/tasks successful")
            post_data = post_response.json()
            todo_id = post_data["task"]["id"]
            print(f"Created todo with ID: {todo_id}")
        elif post_response.status_code == 403:
            print("✗ POST /api/{user_id}/tasks failed with 403 - user ID mismatch")
            print(f"Response: {post_response.text}")
        else:
            print(f"✗ Unexpected response: {post_response.status_code} - {post_response.text}")

        # Test GET /api/{user_id}/tasks/{id} with proper authentication
        if 'todo_id' in locals():
            get_one_response = requests.get(f"http://127.0.0.1:8000/api/{user_id}/tasks/{todo_id}", headers=headers)
            print(f"GET /api/{user_id}/tasks/{todo_id} response: {get_one_response.status_code}")
            if get_one_response.status_code == 200:
                print("✓ GET /api/{user_id}/tasks/{id} successful")
            elif get_one_response.status_code == 403:
                print("✗ GET /api/{user_id}/tasks/{id} failed with 403 - user ID mismatch")
                print(f"Response: {get_one_response.text}")
            else:
                print(f"✗ Unexpected response: {get_one_response.status_code} - {get_one_response.text}")

        # Test PUT /api/{user_id}/tasks/{id} with proper authentication
        if 'todo_id' in locals():
            put_response = requests.put(f"http://127.0.0.1:8000/api/{user_id}/tasks/{todo_id}",
                                     json={"title": "Updated API Test Todo", "description": "Updated test from API", "is_completed": True},
                                     headers=headers)
            print(f"PUT /api/{user_id}/tasks/{todo_id} response: {put_response.status_code}")
            if put_response.status_code in [200, 201]:
                print("✓ PUT /api/{user_id}/tasks/{id} successful")
            elif put_response.status_code == 403:
                print("✗ PUT /api/{user_id}/tasks/{id} failed with 403 - user ID mismatch")
                print(f"Response: {put_response.text}")
            else:
                print(f"✗ Unexpected response: {put_response.status_code} - {put_response.text}")

        # Test PATCH /api/{user_id}/tasks/{id}/complete with proper authentication
        if 'todo_id' in locals():
            patch_response = requests.patch(f"http://127.0.0.1:8000/api/{user_id}/tasks/{todo_id}/complete", headers=headers)
            print(f"PATCH /api/{user_id}/tasks/{todo_id}/complete response: {patch_response.status_code}")
            if patch_response.status_code == 200:
                print("✓ PATCH /api/{user_id}/tasks/{id}/complete successful")
            elif patch_response.status_code == 403:
                print("✗ PATCH /api/{user_id}/tasks/{id}/complete failed with 403 - user ID mismatch")
                print(f"Response: {patch_response.text}")
            else:
                print(f"✗ Unexpected response: {patch_response.status_code} - {patch_response.text}")

        # Test DELETE /api/{user_id}/tasks/{id} with proper authentication
        if 'todo_id' in locals():
            delete_response = requests.delete(f"http://127.0.0.1:8000/api/{user_id}/tasks/{todo_id}", headers=headers)
            print(f"DELETE /api/{user_id}/tasks/{todo_id} response: {delete_response.status_code}")
            if delete_response.status_code == 200:
                print("✓ DELETE /api/{user_id}/tasks/{id} successful")
            elif delete_response.status_code == 403:
                print("✗ DELETE /api/{user_id}/tasks/{id} failed with 403 - user ID mismatch")
                print(f"Response: {delete_response.text}")
            else:
                print(f"✗ Unexpected response: {delete_response.status_code} - {delete_response.text}")

        print("\n[SUCCESS] API endpoint tests completed!")

    finally:
        # Stop the server
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    print("Starting API Endpoint Test Suite...")
    print("=" * 60)

    test_api_endpoints()

    print("=" * 60)
    print("[SUCCESS] API tests completed!")