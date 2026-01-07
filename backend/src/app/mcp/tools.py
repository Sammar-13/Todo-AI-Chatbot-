from typing import Optional, List
from uuid import UUID

from mcp.server.fastmcp import FastMCP
from sqlmodel import select, col
from sqlalchemy.orm import selectinload

from app.database import async_session
from app.db.models import Task, TaskStatus, TaskPriority

# Create an MCP server instance
# We can name it 'todo-server'
mcp = FastMCP("todo-server")

@mcp.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> str:
    """Create a new task for the user."""
    try:
        user_uuid = UUID(user_id)
        async with async_session() as session:
            task = Task(
                user_id=user_uuid,
                title=title,
                description=description,
                status=TaskStatus.PENDING,
                priority=TaskPriority.MEDIUM
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return f"Task created with ID: {task.id}"
    except ValueError:
        return "Error: Invalid user_id format (must be UUID)."
    except Exception as e:
        return f"Error creating task: {str(e)}"

@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    """List tasks for a user. Status can be 'all', 'pending', or 'completed'."""
    try:
        user_uuid = UUID(user_id)
        async with async_session() as session:
            query = select(Task).where(Task.user_id == user_uuid)
            
            if status.lower() == "pending":
                query = query.where(Task.status == TaskStatus.PENDING)
            elif status.lower() == "completed":
                query = query.where(Task.status == TaskStatus.COMPLETED)
                
            # Order by created_at desc
            query = query.order_by(Task.created_at.desc())
            
            result = await session.execute(query)
            tasks = result.scalars().all()
            
            if not tasks:
                return "No tasks found."
            
            task_list = []
            for t in tasks:
                task_list.append(f"[{t.status.value}] {t.title} (ID: {t.id})")
            
            return "\n".join(task_list)
    except ValueError:
        return "Error: Invalid user_id format."
    except Exception as e:
        return f"Error listing tasks: {str(e)}"

@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> str:
    """Mark a task as completed."""
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        async with async_session() as session:
            query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                return f"Task with ID {task_id} not found."
            
            task.status = TaskStatus.COMPLETED
            # task.completed_at = datetime.utcnow() # If model has it
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            return f"Task '{task.title}' marked as completed."
    except ValueError:
        return "Error: Invalid ID format."
    except Exception as e:
        return f"Error completing task: {str(e)}"

@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> str:
    """Permanently remove a task."""
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        async with async_session() as session:
            query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                return f"Task with ID {task_id} not found."
            
            await session.delete(task)
            await session.commit()
            
            return f"Task '{task.title}' deleted."
    except ValueError:
        return "Error: Invalid ID format."
    except Exception as e:
        return f"Error deleting task: {str(e)}"

@mcp.tool()
async def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> str:
    """Update task details."""
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        async with async_session() as session:
            query = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                return f"Task with ID {task_id} not found."
            
            if title:
                task.title = title
            if description:
                task.description = description
                
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            return f"Task '{task.title}' updated."
    except ValueError:
        return "Error: Invalid ID format."
    except Exception as e:
        return f"Error updating task: {str(e)}"
