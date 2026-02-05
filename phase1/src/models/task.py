"""
Task model for the Todo CLI application.

This module defines the Task class which represents a single todo item
with ID, title, description, and status attributes.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, and completion status.

    The Task class provides methods to manage the completion status and
    convert the task to different representations.

    Attributes:
        id (int): Unique identifier for each task, auto-incremented
        title (str): Title of the task, required field that cannot be empty
        description (str): Detailed description of the task, optional field
        status (bool): Completion status (True for complete, False for incomplete)
    """

    id: int
    title: str
    description: Optional[str] = ""
    status: bool = False  # False means incomplete, True means complete

    def __post_init__(self):
        """
        Validate task attributes after initialization.

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

    def mark_complete(self) -> None:
        """
        Mark the task as complete.

        Sets the status attribute to True to indicate the task is complete.
        """
        self.status = True

    def mark_incomplete(self) -> None:
        """
        Mark the task as incomplete.

        Sets the status attribute to False to indicate the task is incomplete.
        """
        self.status = False

    def to_dict(self) -> dict:
        """
        Convert task to dictionary representation.

        Returns:
            dict: A dictionary containing all task attributes with keys
                  'id', 'title', 'description', and 'status'
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    def __str__(self) -> str:
        """
        String representation of the task for display purposes.

        Returns:
            str: Formatted string showing task status, ID, title, and description
        """
        status_str = "✓" if self.status else "○"
        return f"[{status_str}] {self.id}: {self.title} - {self.description}"