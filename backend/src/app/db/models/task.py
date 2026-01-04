"""Task database model (Task 02-027)."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .base import BaseModel


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel, table=True):
    """Task model for todo items.

    Represents a single todo item belonging to a user with status,
    priority, and optional due date tracking.

    Attributes:
        user_id: ID of the user who owns this task
        title: Task title/name
        description: Optional detailed description
        status: Current task status (pending/completed)
        priority: Task priority level (low/medium/high)
        due_date: Optional deadline for task completion
        completed_at: Timestamp when task was completed (null if pending)
    """

    __tablename__ = "tasks"

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="ID of the task owner",
    )
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Detailed task description",
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current task status",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Task priority level",
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional task deadline",
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when task was marked complete",
    )

    # Relationship to User
    user: Optional["User"] = Relationship()

    class Config:
        """Model configuration for composite indexes."""
        # Composite indexes for common query patterns
        # Format: {"index": ["col1", "col2"]} creates INDEX (col1, col2)
        indexes = [
            ("user_id", "status"),  # For: GET /tasks?status_filter=pending
            ("user_id", "priority"),  # For: GET /tasks?priority_filter=high
            ("user_id", "created_at"),  # For: Sorting by creation date
            ("user_id", "due_date"),  # For: Sorting by due date
        ]
