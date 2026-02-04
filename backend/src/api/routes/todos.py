import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from src.models.todo import Todo, TodoBase, TodoCreate, TodoUpdate
from src.models.user import User
from src.database.database import get_session
from src.api.middleware.auth_middleware import get_current_user
from src.api.middleware.error_handler import AuthorizationError, NotFoundError
from src.services.todo_service import TodoService

router = APIRouter()

@router.get("/{user_id}/tasks/{id}")
def get_task(
    user_id: str,
    id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Retrieve a specific task by ID for the specified user.

    Args:
        user_id: ID of the user whose task to retrieve
        id: ID of the task to retrieve
        session: Database session
        current_user: Authenticated user requesting the task

    Returns:
        Dictionary with the requested task

    Raises:
        HTTPException: If task doesn't exist or user doesn't have access
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    try:
        from src.services.todo_service import TodoService
        db_todo = TodoService.get_todo_by_id(
            session=session,
            todo_id=id,
            user=current_user
        )
        return {"task": db_todo}
    except Exception as e:
        if "NotFoundError" in str(type(e)) or "AuthorizationError" in str(type(e)):
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )
        raise e

@router.get("/{user_id}/tasks")
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = Query(None)
) -> dict:
    """
    Retrieve all tasks for the specified user with pagination and optional filtering.

    Args:
        user_id: ID of the user whose tasks to retrieve
        session: Database session
        current_user: Authenticated user requesting tasks
        page: Page number for pagination
        limit: Number of items per page
        completed: Filter by completion status (optional)

    Returns:
        Dictionary with tasks and pagination info
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    tasks, total_count = TodoService.get_user_todos(
        session=session,
        user=current_user,
        completed=completed,
        page=page,
        limit=limit
    )

    # Calculate pagination info
    has_next = (page * limit) < total_count
    has_prev = page > 1

    return {
        "tasks": tasks,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "has_next": has_next,
            "has_prev": has_prev,
            "pages": (total_count + limit - 1) // limit
        }
    }

@router.post("/{user_id}/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create a new task for the specified user.

    Args:
        user_id: ID of the user for whom to create the task
        task_data: Task creation data (title, description, etc.) - user_id is auto-assigned
        session: Database session
        current_user: Authenticated user creating the task

    Returns:
        Dictionary with created task
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create tasks for another user"
        )

    db_task = TodoService.create_todo(
        session=session,
        user=current_user,
        todo_data=task_data
    )

    return {"task": db_task}

@router.put("/{user_id}/tasks/{id}")
def update_task(
    user_id: str,
    id: str,
    task_data: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update an existing task.

    Args:
        user_id: ID of the user whose task to update
        id: ID of the task to update
        task_data: Updated task data (excluding user_id)
        session: Database session
        current_user: Authenticated user updating the task

    Returns:
        Dictionary with updated task

    Raises:
        HTTPException: If task doesn't exist or user doesn't have access
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )

    db_task = TodoService.update_todo(
        session=session,
        todo_id=id,
        user=current_user,
        todo_data=task_data
    )

    return {"task": db_task}

@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: str,
    id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a task.

    Args:
        user_id: ID of the user whose task to delete
        id: ID of the task to delete
        session: Database session
        current_user: Authenticated user deleting the task

    Returns:
        Dictionary with success message

    Raises:
        HTTPException: If task doesn't exist or user doesn't have access
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's tasks"
        )

    success = TodoService.delete_todo(
        session=session,
        todo_id=id,
        user=current_user
    )

    return {
        "success": success,
        "message": "Task deleted successfully"
    }

@router.patch("/{user_id}/tasks/{id}/complete")
def toggle_task_complete(
    user_id: str,
    id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Toggle the completion status of a task.

    Args:
        user_id: ID of the user whose task to toggle
        id: ID of the task to toggle
        session: Database session
        current_user: Authenticated user toggling the task

    Returns:
        Dictionary with updated task

    Raises:
        HTTPException: If task doesn't exist or user doesn't have access
    """
    # Verify the authenticated user matches the requested user_id
    # Compare by converting both to string for consistent comparison
    current_user_id_str = str(current_user.id)
    user_id_str = str(user_id)
    if current_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot toggle another user's tasks"
        )

    db_task = TodoService.toggle_todo_completion(
        session=session,
        todo_id=id,
        user=current_user
    )

    return {"task": db_task}