"""
Utility functions for the Todo CLI application.

This module contains helper functions that are used across the application.
"""


def format_task_status(status: bool) -> str:
    """
    Format the task status for display.

    Args:
        status (bool): The status of the task (True for complete, False for incomplete)

    Returns:
        str: "Complete" if status is True, "Incomplete" otherwise
    """
    return "Complete" if status else "Incomplete"


def validate_task_title(title: str) -> bool:
    """
    Validate if a task title is valid (not empty or just whitespace).

    Args:
        title (str): The title to validate

    Returns:
        bool: True if the title is valid, False otherwise
    """
    return bool(title and title.strip())


def format_task_list(tasks: list) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks (list): List of task objects to format

    Returns:
        str: Formatted string representation of the tasks
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for task in tasks:
        status = "✓" if getattr(task, 'status', False) else "○"
        task_id = getattr(task, 'id', 'N/A')
        title = getattr(task, 'title', 'N/A')
        description = getattr(task, 'description', 'N/A')
        formatted_tasks.append(f"[{status}] {task_id}: {title} - {description}")

    return "\n".join(formatted_tasks)


def get_next_id_from_tasks(tasks: list) -> int:
    """
    Get the next available ID based on existing tasks.

    Args:
        tasks (list): List of existing task objects

    Returns:
        int: The next available ID
    """
    if not tasks:
        return 1
    max_id = max(getattr(task, 'id', 0) for task in tasks)
    return max_id + 1


def get_user_input(prompt: str) -> str:
    """
    Safely get user input with Ctrl+C interruption handling.

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        str: The user input string
    """
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None


def validate_menu_option(option: str, valid_options: list) -> bool:
    """
    Validate if a menu option is valid.

    Args:
        option (str): The option to validate
        valid_options (list): List of valid options

    Returns:
        bool: True if the option is valid, False otherwise
    """
    if not option.isdigit():
        return False
    return int(option) in valid_options


def validate_task_id(task_id: str, max_id: int = None) -> bool:
    """
    Validate if a task ID is valid (positive integer).

    Args:
        task_id (str): The task ID to validate
        max_id (int, optional): Maximum valid ID if known

    Returns:
        bool: True if the task ID is valid, False otherwise
    """
    if not task_id.isdigit():
        return False

    id_num = int(task_id)
    if id_num <= 0:
        return False

    if max_id and id_num > max_id:
        return False

    return True


def format_tasks_table(tasks: list) -> str:
    """
    Format tasks in a table format with ID, title, description, and status.

    Args:
        tasks (list): List of task objects to format

    Returns:
        str: Formatted table string
    """
    if not tasks:
        return "No tasks found."

    # Create table header
    header = f"{'ID':<5} {'Status':<8} {'Title':<25} {'Description':<30}"
    separator = "-" * len(header)

    # Create table rows
    rows = [header, separator]
    for task in tasks:
        status = "✓ Done" if getattr(task, 'status', False) else "○ Todo"
        task_id = str(getattr(task, 'id', 'N/A'))
        title = getattr(task, 'title', 'N/A')[:23]  # Truncate to fit
        description = getattr(task, 'description', 'N/A')[:28]  # Truncate to fit
        row = f"{task_id:<5} {status:<8} {title:<25} {description:<30}"
        rows.append(row)

    return "\n".join(rows)


def validate_non_empty_input(user_input: str) -> bool:
    """
    Validate if user input is not empty or just whitespace.

    Args:
        user_input (str): The input to validate

    Returns:
        bool: True if input is not empty, False otherwise
    """
    return bool(user_input and user_input.strip())


def validate_string_length(user_input: str, max_length: int = 1000) -> bool:
    """
    Validate if string length is within acceptable limits.

    Args:
        user_input (str): The input to validate
        max_length (int): Maximum allowed length

    Returns:
        bool: True if length is acceptable, False otherwise
    """
    return len(user_input) <= max_length