# Phase 3: Todo AI Chatbot - Task List

## Backend & Database

- [ ] **PHASE3-BE-01**: Install Dependencies
    - Add `openai`, `mcp` (or specific SDK package), and any missing db drivers to `backend/requirements.txt`.
- [ ] **PHASE3-BE-02**: Define DB Models
    - Create `backend/src/app/models/conversation.py` (Conversation, Message).
    - Update `backend/src/app/models/__init__.py`.
- [ ] **PHASE3-BE-03**: Database Migrations
    - Generate Alembic migration script.
    - Apply migration to local/dev DB.

## MCP Tools

- [ ] **PHASE3-MCP-01**: Setup MCP Server
    - Initialize MCP server instance in `backend/src/app/mcp_server.py`.
- [ ] **PHASE3-MCP-02**: Implement Task Tools
    - Write functions for `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
    - Decorate/Register them with the MCP server.
    - Ensure they interact correctly with the DB (dependency injection context).

## Agent & API

- [ ] **PHASE3-API-01**: Chat Endpoint Logic
    - Create `backend/src/app/api/routes/chat.py`.
    - Implement `POST /` handler.
    - Logic: Load history -> Init Agent -> Run Agent -> Save History.
- [ ] **PHASE3-API-02**: Agent Integration
    - Configure OpenAI Client/Agent.
    - Bind MCP tools to the Agent.
    - Handle tool execution loop (if not auto-handled by SDK).
- [ ] **PHASE3-API-03**: Register Router
    - Add chat router to `backend/src/app/main.py`.

## Frontend

- [ ] **PHASE3-FE-01**: Chat Component
    - Create `frontend/src/components/Chat/ChatInterface.tsx`.
    - UI for message list and input.
- [ ] **PHASE3-FE-02**: Chat Service
    - Add API call logic in `frontend/src/services/chatService.ts` (or similar).
- [ ] **PHASE3-FE-03**: Page Integration
    - Add Chat component to a new page (e.g., `/chat`) or embedded in the Dashboard.

## Finalization

- [ ] **PHASE3-FIN-01**: End-to-End Test
    - Verify conversation flow and task updates.
- [ ] **PHASE3-FIN-02**: Documentation
    - Update README with new env vars (`OPENAI_API_KEY`) and usage instructions.