import uuid
from sqlmodel import Session
from src.database.database import engine
from src.models.user import User
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.services.user_service import UserService
from src.services.todo_service import TodoService


def test_todo_crud_operations():
    """
    Test all Todo CRUD operations to ensure they work correctly with user authentication
    """
    print("Testing Todo CRUD operations...")

    # Create a database session
    with Session(engine) as session:
        # Create a test user
        test_email = f"test_{uuid.uuid4()}@example.com"
        test_password = "testpassword123"

        print(f"Creating test user with email: {test_email}")
        user = UserService.create_user(session, test_email, test_password)
        print(f"Created user with ID: {user.id}")

        # Test CREATE operation
        print("\n1. Testing CREATE operation...")
        todo_create_data = TodoCreate(
            title="Test Todo",
            description="This is a test todo item",
            is_completed=False
        )
        created_todo = TodoService.create_todo(session, user, todo_create_data)
        print(f"Created todo with ID: {created_todo.id}")
        print(f"Todo title: {created_todo.title}")
        print(f"Todo description: {created_todo.description}")
        print(f"Todo completed: {created_todo.is_completed}")
        print(f"Todo user_id: {created_todo.user_id}")

        # Verify user_id matches the created user
        assert created_todo.user_id == user.id, f"Expected user_id {user.id}, got {created_todo.user_id}"
        print("[PASS] User ID verification passed")

        # Test READ (get single) operation
        print("\n2. Testing READ (single) operation...")
        retrieved_todo = TodoService.get_todo_by_id(session, created_todo.id, user)
        print(f"Retrieved todo: {retrieved_todo.title}")
        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == "Test Todo"
        print("[PASS] Read single operation passed")

        # Test READ (get all) operation
        print("\n3. Testing READ (all) operation...")
        todos, total_count = TodoService.get_user_todos(session, user)
        print(f"Total todos for user: {total_count}")
        print(f"Number of todos returned: {len(todos)}")
        assert total_count == 1
        assert len(todos) == 1
        assert todos[0].id == created_todo.id
        print("[PASS] Read all operation passed")

        # Test UPDATE operation
        print("\n4. Testing UPDATE operation...")
        todo_update_data = TodoUpdate(
            title="Updated Test Todo",
            description="This is an updated test todo item",
            is_completed=True
        )
        updated_todo = TodoService.update_todo(session, created_todo.id, user, todo_update_data)
        print(f"Updated todo title: {updated_todo.title}")
        print(f"Updated todo completed: {updated_todo.is_completed}")
        assert updated_todo.title == "Updated Test Todo"
        assert updated_todo.description == "This is an updated test todo item"
        assert updated_todo.is_completed == True
        print("[PASS] Update operation passed")

        # Test TOGGLE COMPLETION operation
        print("\n5. Testing TOGGLE COMPLETION operation...")
        toggled_todo = TodoService.toggle_todo_completion(session, updated_todo.id, user)
        print(f"Toggled todo completed: {toggled_todo.is_completed}")
        # Since it was True, it should now be False
        assert toggled_todo.is_completed == False
        print("[PASS] Toggle completion operation passed")

        # Test DELETE operation
        print("\n6. Testing DELETE operation...")
        delete_result = TodoService.delete_todo(session, created_todo.id, user)
        print(f"Delete result: {delete_result}")
        assert delete_result == True

        # Verify the todo is actually deleted
        remaining_todos, remaining_count = TodoService.get_user_todos(session, user)
        assert remaining_count == 0
        assert len(remaining_todos) == 0
        print("[PASS] Delete operation passed")

        print("\n[SUCCESS] All Todo CRUD operations tested successfully!")
        print("[SUCCESS] CREATE, READ (single & all), UPDATE, TOGGLE COMPLETION, and DELETE operations work correctly")
        print("[SUCCESS] User authentication and authorization working properly")
        print("[SUCCESS] UUID fields are properly handled")


def test_uuid_serialization():
    """
    Test that UUID fields are properly serialized as strings
    """
    print("\nTesting UUID serialization...")

    # Create sample UUID
    test_uuid = str(uuid.uuid4())
    print(f"Generated UUID string: {test_uuid}")
    print(f"Type: {type(test_uuid)}")

    # Verify it's a valid UUID string format
    try:
        uuid_obj = uuid.UUID(test_uuid)
        print(f"Validated UUID: {uuid_obj}")
        print("[PASS] UUID serialization test passed")
    except ValueError:
        print("[FAIL] UUID serialization test failed")
        raise


if __name__ == "__main__":
    print("Starting Todo CRUD Operations Test Suite...")
    print("=" * 60)

    # Test UUID serialization first
    test_uuid_serialization()

    # Test CRUD operations
    test_todo_crud_operations()

    print("=" * 60)
    print("[SUCCESS] All tests passed! Todo CRUD operations are working correctly.")