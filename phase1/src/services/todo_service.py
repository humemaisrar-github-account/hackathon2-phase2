"""
TodoService for the Todo CLI application.

This module contains the business logic for CRUD operations on tasks.
It manages in-memory storage and provides methods for all required
operations: Add, View, Update, Delete, and Mark Complete/Incomplete.
"""

from typing import Dict, List, Optional
from src.models.task import Task


class TodoService:
    """
    Service class that handles business logic for todo operations.

    This class manages the in-memory storage of tasks using a dictionary
    for O(1) lookup by ID and maintains sequential ID generation.
    It provides all the core functionality for task management including
    adding, retrieving, updating, deleting, and marking tasks as complete/incomplete.

    Attributes:
        _tasks (Dict[int, Task]): Dictionary mapping task IDs to Task objects
        _next_id (int): The next available ID for new tasks
    """

    def __init__(self) -> None:
        """
        Initialize the TodoService with an empty task collection.

        Sets up the internal storage dictionary and initializes the next ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with unique ID and initial "incomplete" status.

        Creates a new Task object with the provided title and description,
        assigns the next available unique ID, and stores it in the in-memory collection.

        Args:
            title (str): Title of the task (required, cannot be empty)
            description (str): Description of the task (optional, defaults to empty string)

        Returns:
            Task: The newly created task object with assigned ID and initial status

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
            status=False  # Initially incomplete
        )

        self._tasks[task.id] = task
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Looks up a task in the in-memory collection using its unique ID.

        Args:
            task_id (int): The unique identifier of the task to retrieve

        Returns:
            Task: The task object if found, None if no task exists with the given ID
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in insertion order (by ID).

        Returns all tasks sorted by their ID to maintain consistent ordering.

        Returns:
            List[Task]: List of all tasks sorted by ID in ascending order
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]:
        """
        Update the title or description of an existing task by ID.

        Modifies the specified attributes of a task if it exists.
        Only the provided attributes are updated; others remain unchanged.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task (if provided)
            description (str, optional): New description for the task (if provided)

        Returns:
            Task: The updated task object if successful, None if task doesn't exist

        Raises:
            ValueError: If a new title is provided but is empty or contains only whitespace
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description else ""

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID from the in-memory collection.

        Deletes the specified task if it exists in the collection.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was successfully deleted, False if task didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by its ID.

        Updates the status of the specified task to complete (True).

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            bool: True if task was marked complete, False if task didn't exist
        """
        task = self._tasks.get(task_id)
        if task:
            task.status = True
            return True
        return False

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by its ID.

        Updates the status of the specified task to incomplete (False).

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            bool: True if task was marked incomplete, False if task didn't exist
        """
        task = self._tasks.get(task_id)
        if task:
            task.status = False
            return True
        return False

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns the ID that will be assigned to the next task added to the service.

        Returns:
            int: The next available ID
        """
        return self._next_id