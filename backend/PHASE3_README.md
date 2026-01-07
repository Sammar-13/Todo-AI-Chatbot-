# Hackathon Todo Backend - Phase 3

## Overview
This is the backend for the Hackathon Todo app, now featuring an AI-powered Chatbot (Phase 3).
It uses FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, and MCP.

## Setup

1.  **Install Dependencies**
    ```bash
    cd backend
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Environment Variables**
    Create `.env` in `backend/` directory:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
    # Or for local testing (if allowed):
    # DATABASE_URL=sqlite+aiosqlite:///./backend_local.db
    
    OPENAI_API_KEY=sk-proj-....
    
    JWT_SECRET_KEY=your_secret_key
    ENVIRONMENT=development
    DEBUG=True
    ```

3.  **Database Migrations**
    ```bash
    # If using local SQLite or if DB is reachable
    alembic upgrade head
    ```

## Running Locally
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## Phase 3 Features
-   **Chat Endpoint**: `POST /api/{user_id}/chat`
-   **AI Agent**: Manages tasks via natural language using OpenAI GPT-4o.
-   **MCP Tools**:
    -   `add_task`
    -   `list_tasks`
    -   `complete_task`
    -   `delete_task`
    -   `update_task`

## Deployment
1.  **Vercel**:
    -   Deploy as a Python Serverless Function.
    -   Ensure `requirements.txt` is present.
    -   Set Environment Variables in Vercel Dashboard.
2.  **Neon**:
    -   Ensure `DATABASE_URL` uses the pooled connection string from Neon.
    -   Run migrations locally against the Neon DB or use a migration job.
