"""Task request/response schemas (Task 02-033)."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..db.models import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Task creation request schema.

    Attributes:
        title: Task title (required)
        description: Detailed task description (optional)
        priority: Task priority level (default: medium)
        due_date: Optional task deadline
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title",
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed task description",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Task priority level",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional task deadline",
    )


class TaskUpdate(BaseModel):
    """Task update request schema.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated task title
        description: Updated description
        status: Updated task status
        priority: Updated priority level
        due_date: Updated due date
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Updated task title",
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Updated description",
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="Updated task status",
    )
    priority: Optional[TaskPriority] = Field(
        None,
        description="Updated priority level",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Updated due date",
    )


class TaskRead(BaseModel):
    """Task read response schema.

    Attributes:
        id: Task's unique identifier
        user_id: ID of task owner
        title: Task title
        description: Task description
        status: Current task status
        priority: Task priority level
        due_date: Optional deadline
        created_at: Task creation timestamp
        updated_at: Last update timestamp
        completed_at: Completion timestamp (if completed)
    """

    id: UUID = Field(..., description="Unique task ID")
    user_id: UUID = Field(..., description="Task owner ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(..., description="Current task status")
    priority: TaskPriority = Field(..., description="Priority level")
    due_date: Optional[datetime] = Field(None, description="Deadline")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class TaskListResponse(BaseModel):
    """Paginated task list response.

    Attributes:
        items: List of tasks
        total: Total number of tasks matching filters
        skip: Number of items skipped
        limit: Maximum items per page
    """

    items: List[TaskRead] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total tasks matching filters")
    skip: int = Field(default=0, description="Items skipped")
    limit: int = Field(default=10, description="Items per page")
