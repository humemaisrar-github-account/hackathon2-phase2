"""
Interactive CLI entry point for the Todo CLI application.

This module provides an interactive command-line interface for managing todo tasks.
Users can navigate through a menu system to add, view, update, delete, and manage task completion status.
"""
import sys
from typing import Optional
from src.services.todo_service import TodoService
from src.lib.utils import (
    format_tasks_table,
    validate_menu_option,
    validate_task_id,
    validate_non_empty_input,
    get_user_input
)


def display_menu() -> None:
    """
    Display the main menu with numbered options.
    """
    print("\n" + "="*50)
    print("           TODO CLI APPLICATION")
    print("="*50)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print("="*50)


def get_user_choice() -> str:
    """
    Get and validate user menu choice.

    Returns:
        str: The user's menu choice (1-6) or None if interrupted
    """
    choice = get_user_input("Please select an option (1-6): ")
    return choice


def handle_add_task(service: TodoService) -> None:
    """
    Handle adding a new task through the interactive menu.

    Args:
        service (TodoService): The todo service instance
    """
    print("\n--- Add New Task ---")

    title = get_user_input("Enter task title: ")
    if title is None:  # User cancelled with Ctrl+C
        return

    if not validate_non_empty_input(title):
        print("Error: Task title cannot be empty.")
        return

    description = get_user_input("Enter task description (optional): ")
    if description is None:  # User cancelled with Ctrl+C
        return

    try:
        task = service.add_task(title, description)
        print(f"\n✓ Task added successfully!")
        print(f"ID: {task.id}, Title: {task.title}, Description: {task.description}, Status: {'Complete' if task.status else 'Incomplete'}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_view_tasks(service: TodoService) -> None:
    """
    Handle viewing all tasks through the interactive menu.

    Args:
        service (TodoService): The todo service instance
    """
    print("\n--- View Tasks ---")
    tasks = service.get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    formatted_tasks = format_tasks_table(tasks)
    print(formatted_tasks)


def handle_update_task(service: TodoService) -> None:
    """
    Handle updating a task through the interactive menu.

    Args:
        service (TodoService): The todo service instance
    """
    print("\n--- Update Task ---")

    # Get task ID
    task_id_str = get_user_input("Enter task ID to update: ")
    if task_id_str is None:  # User cancelled with Ctrl+C
        return

    # Validate task ID
    all_tasks = service.get_all_tasks()
    max_id = max([getattr(task, 'id', 0) for task in all_tasks], default=0)

    if not validate_task_id(task_id_str, max_id):
        print(f"Error: Invalid task ID. Please enter a number between 1 and {max_id}.")
        return

    task_id = int(task_id_str)

    # Check if task exists
    task = service.get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Get new title
    new_title = get_user_input(f"Enter new title (current: '{task.title}'): ")
    if new_title is None:  # User cancelled with Ctrl+C
        return

    if not validate_non_empty_input(new_title):
        print("Error: Task title cannot be empty.")
        return

    # Get new description
    new_description = get_user_input(f"Enter new description (current: '{task.description}'): ")
    if new_description is None:  # User cancelled with Ctrl+C
        return

    # Update the task
    updated_task = service.update_task(task_id, new_title, new_description)
    if updated_task:
        print(f"\n✓ Task {task_id} updated successfully!")
        print(f"Title: {updated_task.title}, Description: {updated_task.description}")
    else:
        print(f"Error: Failed to update task with ID {task_id}.")


def handle_delete_task(service: TodoService) -> None:
    """
    Handle deleting a task through the interactive menu.

    Args:
        service (TodoService): The todo service instance
    """
    print("\n--- Delete Task ---")

    # Get task ID
    task_id_str = get_user_input("Enter task ID to delete: ")
    if task_id_str is None:  # User cancelled with Ctrl+C
        return

    # Validate task ID
    all_tasks = service.get_all_tasks()
    max_id = max([getattr(task, 'id', 0) for task in all_tasks], default=0)

    if not validate_task_id(task_id_str, max_id):
        print(f"Error: Invalid task ID. Please enter a number between 1 and {max_id}.")
        return

    task_id = int(task_id_str)

    # Check if task exists
    task = service.get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Confirm deletion
    confirm = get_user_input(f"Are you sure you want to delete task '{task.title}'? (y/N): ")
    if confirm is None:  # User cancelled with Ctrl+C
        return

    if confirm.lower() in ['y', 'yes']:
        success = service.delete_task(task_id)
        if success:
            print(f"\n✓ Task {task_id} deleted successfully!")
        else:
            print(f"Error: Failed to delete task with ID {task_id}.")
    else:
        print("Deletion cancelled.")


def handle_toggle_completion(service: TodoService) -> None:
    """
    Handle toggling task completion status through the interactive menu.

    Args:
        service (TodoService): The todo service instance
    """
    print("\n--- Mark Task Complete/Incomplete ---")

    # Get task ID
    task_id_str = get_user_input("Enter task ID: ")
    if task_id_str is None:  # User cancelled with Ctrl+C
        return

    # Validate task ID
    all_tasks = service.get_all_tasks()
    max_id = max([getattr(task, 'id', 0) for task in all_tasks], default=0)

    if not validate_task_id(task_id_str, max_id):
        print(f"Error: Invalid task ID. Please enter a number between 1 and {max_id}.")
        return

    task_id = int(task_id_str)

    # Check if task exists
    task = service.get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Ask for completion status
    current_status = "Complete" if task.status else "Incomplete"
    print(f"Current status for task '{task.title}': {current_status}")

    status_choice = get_user_input("Mark as (1) Complete or (2) Incomplete: ")
    if status_choice is None:  # User cancelled with Ctrl+C
        return

    if status_choice == "1":
        success = service.mark_task_complete(task_id)
        if success:
            print(f"\n✓ Task {task_id} marked as complete!")
        else:
            print(f"Error: Failed to mark task {task_id} as complete.")
    elif status_choice == "2":
        success = service.mark_task_incomplete(task_id)
        if success:
            print(f"\n✓ Task {task_id} marked as incomplete!")
        else:
            print(f"Error: Failed to mark task {task_id} as incomplete.")
    else:
        print("Invalid choice. Please enter 1 for Complete or 2 for Incomplete.")


def main_menu_loop() -> None:
    """
    Main interactive menu loop that continues until user selects Exit.
    """
    service = TodoService()

    while True:
        try:
            display_menu()
            choice = get_user_input("Please select an option (1-6): ")

            if choice is None:  # User cancelled with Ctrl+C at menu level
                print("\nExiting application...")
                break

            valid_options = [1, 2, 3, 4, 5, 6]
            if not validate_menu_option(choice, valid_options):
                print(f"\nInvalid option. Please select a number between 1 and {len(valid_options)}.")
                continue

            choice_num = int(choice)

            if choice_num == 1:
                handle_add_task(service)
            elif choice_num == 2:
                handle_view_tasks(service)
            elif choice_num == 3:
                handle_update_task(service)
            elif choice_num == 4:
                handle_delete_task(service)
            elif choice_num == 5:
                handle_toggle_completion(service)
            elif choice_num == 6:
                print("\nThank you for using the Todo CLI Application. Goodbye!")
                break

            # Pause before showing menu again
            input("\nPress Enter to return to the main menu...")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            input("\nPress Enter to continue...")


def main() -> None:
    """
    Main entry point for the interactive CLI application.
    """
    print("Welcome to the Todo CLI Application!")
    main_menu_loop()


if __name__ == "__main__":
    main()