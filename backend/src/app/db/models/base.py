"""Base model with common fields for all database models."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base model with common fields for all database models.

    Provides automatic UUID generation, creation and update timestamps.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique identifier")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Last update timestamp"
    )
