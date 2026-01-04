"""Task management API routes (Tasks 02-034 to 02-039)."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import get_session
from ...db.models import Task, TaskPriority, TaskStatus, User
from ...schemas import TaskCreate, TaskListResponse, TaskRead, TaskUpdate
from ...services.task import (
    create_task,
    delete_task,
    get_task_by_id,
    get_user_tasks,
    update_task,
)
from ..dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, ge=0, description="Items to skip (pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status_filter: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority_filter: Optional[TaskPriority] = Query(None, description="Filter by priority"),
) -> TaskListResponse:
    """List tasks with pagination and filtering (Task 02-034).

    Args:
        current_user: Currently authenticated user
        session: Database session
        skip: Number of items to skip
        limit: Maximum items to return
        status_filter: Optional status filter
        priority_filter: Optional priority filter

    Returns:
        TaskListResponse with paginated tasks
    """
    try:
        tasks, total = await get_user_tasks(
            session,
            current_user.id,
            skip=skip,
            limit=limit,
            status_filter=status_filter,
            priority_filter=priority_filter,
        )

        return TaskListResponse(
            items=[TaskRead.model_validate(task) for task in tasks],
            total=total,
            skip=skip,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    request: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    """Create a new task (Task 02-035).

    Args:
        request: TaskCreate request with title, description, priority, due_date
        current_user: Currently authenticated user
        session: Database session

    Returns:
        Created TaskRead object

    Raises:
        HTTPException: 400 if validation fails
    """
    try:
        task = await create_task(
            session,
            user_id=current_user.id,
            title=request.title,
            description=request.description,
            priority=request.priority,
            due_date=request.due_date,
        )

        return TaskRead.model_validate(task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    """Get task by ID (Task 02-036).

    Args:
        task_id: UUID of task to retrieve
        current_user: Currently authenticated user
        session: Database session

    Returns:
        TaskRead object

    Raises:
        HTTPException: 400 if task_id invalid, 404 if not found or unauthorized
    """
    try:
        from uuid import UUID

        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )

    task = await get_task_by_id(session, task_uuid, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    task_id: str,
    request: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    """Update task (Task 02-037).

    Args:
        task_id: UUID of task to update
        request: TaskUpdate with fields to update
        current_user: Currently authenticated user
        session: Database session

    Returns:
        Updated TaskRead object

    Raises:
        HTTPException: 400 if invalid, 404 if not found or unauthorized
    """
    try:
        from uuid import UUID

        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )

    try:
        # Prepare updates dictionary
        updates = {}
        if request.title is not None:
            updates["title"] = request.title
        if request.description is not None:
            updates["description"] = request.description
        if request.status is not None:
            updates["status"] = request.status
        if request.priority is not None:
            updates["priority"] = request.priority
        if request.due_date is not None:
            updates["due_date"] = request.due_date

        task = await update_task(session, task_uuid, current_user.id, updates)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return TaskRead.model_validate(task)
    except ValueError as e:
        error_msg = str(e)
        if "Cannot update" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg,
            ) from e
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from e


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete task (Task 02-038).

    Args:
        task_id: UUID of task to delete
        current_user: Currently authenticated user
        session: Database session

    Raises:
        HTTPException: 400 if task_id invalid, 404 if not found or unauthorized
    """
    try:
        from uuid import UUID

        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )

    success = await delete_task(session, task_uuid, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
