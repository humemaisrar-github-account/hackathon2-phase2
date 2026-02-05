"""
Unit tests for the TodoService.

This module contains unit tests for the TodoService class to ensure proper functionality.
"""

import pytest
from src.services.todo_service import TodoService
from src.models.task import Task


def test_add_task_success():
    """Test adding a task successfully."""
    service = TodoService()

    task = service.add_task("Test Title", "Test Description")

    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.status is False  # Should be incomplete by default
    assert len(service.get_all_tasks()) == 1


def test_add_task_without_description():
    """Test adding a task without description."""
    service = TodoService()

    task = service.add_task("Test Title")

    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == ""
    assert task.status is False


def test_add_task_empty_title():
    """Test that adding a task with empty title raises ValueError."""
    service = TodoService()

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.add_task("")


def test_add_task_whitespace_title():
    """Test that adding a task with whitespace-only title raises ValueError."""
    service = TodoService()

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.add_task("   ")


def test_get_task_exists():
    """Test getting a task that exists."""
    service = TodoService()
    task = service.add_task("Test Title", "Test Description")

    retrieved_task = service.get_task(task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == task.title


def test_get_task_not_exists():
    """Test getting a task that doesn't exist."""
    service = TodoService()

    retrieved_task = service.get_task(999)

    assert retrieved_task is None


def test_get_all_tasks_empty():
    """Test getting all tasks when none exist."""
    service = TodoService()

    tasks = service.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_multiple():
    """Test getting all tasks when multiple exist."""
    service = TodoService()
    task1 = service.add_task("Task 1", "Description 1")
    task2 = service.add_task("Task 2", "Description 2")
    task3 = service.add_task("Task 3", "Description 3")

    tasks = service.get_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].id == task1.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task3.id
    # Tasks should be sorted by ID


def test_update_task_success():
    """Test updating a task successfully."""
    service = TodoService()
    original_task = service.add_task("Original Title", "Original Description")

    updated_task = service.update_task(original_task.id, "New Title", "New Description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_partial():
    """Test updating only title or description of a task."""
    service = TodoService()
    original_task = service.add_task("Original Title", "Original Description")

    # Update only title
    updated_task = service.update_task(original_task.id, title="New Title")

    assert updated_task is not None
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged


def test_update_task_not_exists():
    """Test updating a task that doesn't exist."""
    service = TodoService()

    result = service.update_task(999, "New Title", "New Description")

    assert result is None


def test_update_task_empty_title():
    """Test that updating a task with empty title raises ValueError."""
    service = TodoService()
    original_task = service.add_task("Original Title", "Original Description")

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.update_task(original_task.id, "")


def test_delete_task_success():
    """Test deleting a task successfully."""
    service = TodoService()
    task = service.add_task("Test Title", "Test Description")

    result = service.delete_task(task.id)

    assert result is True
    assert len(service.get_all_tasks()) == 0


def test_delete_task_not_exists():
    """Test deleting a task that doesn't exist."""
    service = TodoService()

    result = service.delete_task(999)

    assert result is False


def test_mark_task_complete():
    """Test marking a task as complete."""
    service = TodoService()
    task = service.add_task("Test Title", "Test Description")

    result = service.mark_task_complete(task.id)

    assert result is True
    assert task.status is True


def test_mark_task_complete_not_exists():
    """Test marking a non-existent task as complete."""
    service = TodoService()

    result = service.mark_task_complete(999)

    assert result is False


def test_mark_task_incomplete():
    """Test marking a task as incomplete."""
    service = TodoService()
    task = service.add_task("Test Title", "Test Description")
    # First mark it complete
    service.mark_task_complete(task.id)

    result = service.mark_task_incomplete(task.id)

    assert result is True
    assert task.status is False


def test_mark_task_incomplete_not_exists():
    """Test marking a non-existent task as incomplete."""
    service = TodoService()

    result = service.mark_task_incomplete(999)

    assert result is False


def test_get_next_id():
    """Test getting the next available ID."""
    service = TodoService()

    next_id = service.get_next_id()

    assert next_id == 1

    # Add a task and check again
    service.add_task("Test Title", "Test Description")
    next_id = service.get_next_id()

    assert next_id == 2