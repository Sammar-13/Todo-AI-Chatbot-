"""Migration: Add composite indexes to tasks table for performance optimization."""

from sqlalchemy import text


def upgrade(connection):
    """Create composite indexes on tasks table."""
    # Index for filtering by status
    connection.execute(text(
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks(user_id, status)"
    ))

    # Index for filtering by priority
    connection.execute(text(
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_priority ON tasks(user_id, priority)"
    ))

    # Index for sorting by created_at
    connection.execute(text(
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_created ON tasks(user_id, created_at DESC)"
    ))

    # Index for sorting by due_date
    connection.execute(text(
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_due_date ON tasks(user_id, due_date)"
    ))


def downgrade(connection):
    """Drop composite indexes."""
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_status"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_priority"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_created"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_due_date"))
