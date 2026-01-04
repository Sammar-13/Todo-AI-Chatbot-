"""Task service with business logic (Task 02-031)."""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.models import Task, TaskPriority, TaskStatus


def _build_task_query(
    user_id: UUID,
    status_filter: Optional[TaskStatus] = None,
    priority_filter: Optional[TaskPriority] = None,
):
    """Build a reusable query for filtering tasks.

    Args:
        user_id: User ID to filter by
        status_filter: Optional status filter
        priority_filter: Optional priority filter

    Returns:
        SQLModel select statement with filters applied
    """
    statement = select(Task).where(Task.user_id == user_id)

    if status_filter:
        statement = statement.where(Task.status == status_filter)

    if priority_filter:
        statement = statement.where(Task.priority == priority_filter)

    return statement


async def create_task(
    session: AsyncSession,
    user_id: UUID,
    title: str,
    description: Optional[str] = None,
    priority: TaskPriority = TaskPriority.MEDIUM,
    due_date: Optional[datetime] = None,
) -> Task:
    """Create a new task for user (Task 02-031).

    Args:
        session: Database session
        user_id: UUID of task owner
        title: Task title
        description: Optional task description
        priority: Task priority level
        due_date: Optional task deadline

    Returns:
        Created Task object

    Raises:
        ValueError: If validation fails
    """
    if not user_id or not title:
        raise ValueError("User ID and title are required")

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        status=TaskStatus.PENDING,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def get_user_tasks(
    session: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    status_filter: Optional[TaskStatus] = None,
    priority_filter: Optional[TaskPriority] = None,
) -> tuple[List[Task], int]:
    """Get all tasks for a user with optional filtering (Task 02-031).

    Uses a single database query with window functions to get both
    paginated results and total count, eliminating N+1 query problem.

    Args:
        session: Database session
        user_id: UUID of task owner
        skip: Number of items to skip (pagination)
        limit: Maximum items to return
        status_filter: Optional filter by status
        priority_filter: Optional filter by priority

    Returns:
        Tuple of (tasks list, total count)

    Raises:
        ValueError: If pagination parameters are invalid
    """
    if skip < 0 or limit < 1 or limit > 100:
        raise ValueError("Skip must be >= 0 and limit must be 1-100")

    # Build the base query
    statement = _build_task_query(user_id, status_filter, priority_filter)

    # Add window function to count total matching rows without pagination
    # This gets the total count in the same query as the paginated results
    total_count = func.count(Task.id).over()

    # Select both the task data and total count
    from sqlalchemy.sql import literal_column
    statement = select(
        Task,
        total_count.label("_total_count")
    ).select_from(Task).where(Task.user_id == user_id)

    # Apply filters
    if status_filter:
        statement = statement.where(Task.status == status_filter)
    if priority_filter:
        statement = statement.where(Task.priority == priority_filter)

    # Order and paginate
    statement = statement.order_by(Task.created_at.desc()).offset(skip).limit(limit)

    # Execute single query
    result = await session.execute(statement)
    rows = result.all()

    if not rows:
        return [], 0

    # Extract tasks and total from first row
    tasks = [row[0] for row in rows]
    total = rows[0][1] if rows else 0

    return tasks, total


async def get_task_by_id(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
) -> Optional[Task]:
    """Get task by ID with ownership verification (Task 02-031).

    Args:
        session: Database session
        task_id: UUID of task to retrieve
        user_id: UUID of user (for ownership check)

    Returns:
        Task object if found and user is owner, None otherwise
    """
    if not task_id or not user_id:
        return None

    task = await session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None

    return task


async def update_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
    updates: dict,
) -> Optional[Task]:
    """Update task with ownership verification (Task 02-031).

    Args:
        session: Database session
        task_id: UUID of task to update
        user_id: UUID of user (for ownership check)
        updates: Dictionary of fields to update

    Returns:
        Updated Task object if found, None otherwise

    Raises:
        ValueError: If updates are invalid
    """
    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Allowed fields
    allowed_fields = {"title", "description", "status", "priority", "due_date"}

    for field, value in updates.items():
        if field not in allowed_fields:
            raise ValueError(f"Cannot update field: {field}")

        if value is not None:
            # Handle status change - set completed_at if completing
            if field == "status" and value == TaskStatus.COMPLETED:
                task.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
            elif field == "status" and value == TaskStatus.PENDING:
                task.completed_at = None

            setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
) -> bool:
    """Delete task with ownership verification (Task 02-031).

    Args:
        session: Database session
        task_id: UUID of task to delete
        user_id: UUID of user (for ownership check)

    Returns:
        True if task deleted, False if not found or unauthorized

    Raises:
        ValueError: If operation fails
    """
    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()

    return True
