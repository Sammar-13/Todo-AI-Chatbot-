from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from .base import BaseModel

class Conversation(BaseModel, table=True):
    """Conversation model for storing chat history."""
    
    __tablename__ = "conversations"
    
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete"})
    user: Optional["User"] = Relationship()


class Message(BaseModel, table=True):
    """Message model for storing individual chat messages."""
    
    __tablename__ = "messages"
    
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(foreign_key="users.id")
    role: str = Field(description="Role of the message sender: user, assistant, system")
    content: str = Field(description="Content of the message")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship()
