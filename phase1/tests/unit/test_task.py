"""
Unit tests for the Task model.

This module contains unit tests for the Task class to ensure proper functionality.
"""

import pytest
from src.models.task import Task


def test_task_creation_with_valid_data():
    """Test creating a task with valid data."""
    task = Task(id=1, title="Test Task", description="Test Description", status=False)

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status is False


def test_task_creation_with_defaults():
    """Test creating a task with default values."""
    task = Task(id=1, title="Test Task")

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.status is False


def test_task_creation_empty_title():
    """Test that creating a task with empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(id=1, title="")


def test_task_creation_whitespace_title():
    """Test that creating a task with whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(id=1, title="   ")


def test_task_mark_complete():
    """Test marking a task as complete."""
    task = Task(id=1, title="Test Task")

    task.mark_complete()

    assert task.status is True


def test_task_mark_incomplete():
    """Test marking a task as incomplete."""
    task = Task(id=1, title="Test Task", status=True)

    task.mark_incomplete()

    assert task.status is False


def test_task_to_dict():
    """Test converting task to dictionary."""
    task = Task(id=1, title="Test Task", description="Test Description", status=True)
    expected_dict = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "status": True
    }

    assert task.to_dict() == expected_dict


def test_task_str_representation():
    """Test string representation of a task."""
    task = Task(id=1, title="Test Task", description="Test Description", status=True)
    expected_str = "[✓] 1: Test Task - Test Description"

    assert str(task) == expected_str


def test_task_str_representation_incomplete():
    """Test string representation of an incomplete task."""
    task = Task(id=1, title="Test Task", description="Test Description", status=False)
    expected_str = "[○] 1: Test Task - Test Description"

    assert str(task) == expected_str