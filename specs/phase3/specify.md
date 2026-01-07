# Phase 3: Todo AI Chatbot - Specification

## Architecture Overview
The system follows a stateless, agentic architecture where a FastAPI backend orchestrates interactions between the OpenAI Agent, an MCP Server exposing tools, and a Neon PostgreSQL database.

### High-Level Flow
1.  **Request**: Client sends `POST /api/{user_id}/chat` with a message.
2.  **Context Loading**: Backend fetches existing conversation history from DB.
3.  **Agent Execution**:
    -   Agent is initialized with the fetched history.
    -   Agent processes the user message.
    -   Agent decides to call tools (MCP) if necessary.
4.  **Tool Execution**:
    -   MCP Server executes the requested tool (`add_task`, etc.).
    -   Tool interacts with the Database (CRUD operations).
    -   Tool returns result to the Agent.
5.  **Response**:
    -   Agent generates a natural language response.
    -   New message and tool calls are saved to DB.
    -   Response is sent back to the client.

## Database Models (SQLModel)

### Task (Existing/Refined)
-   `id`: Integer, Primary Key
-   `user_id`: String, Index
-   `title`: String
-   `description`: String (Optional)
-   `completed`: Boolean
-   `created_at`: DateTime
-   `updated_at`: DateTime

### Conversation
-   `id`: Integer, Primary Key
-   `user_id`: String, Index
-   `title`: String (Optional, auto-generated summary)
-   `created_at`: DateTime
-   `updated_at`: DateTime

### Message
-   `id`: Integer, Primary Key
-   `conversation_id`: Integer, Foreign Key -> Conversation
-   `user_id`: String
-   `role`: String (`user`, `assistant`, `system`)
-   `content`: Text
-   `tool_calls`: JSON (Optional, stores MCP tool invocations)
-   `created_at`: DateTime

## API Endpoints

### Chat Endpoint
-   **Method**: `POST`
-   **Path**: `/api/{user_id}/chat`
-   **Request Body**:
    ```json
    {
      "conversation_id": "optional_int",
      "message": "string"
    }
    ```
-   **Response**:
    ```json
    {
      "conversation_id": "int",
      "response": "string",
      "tool_calls": [ ... ]
    }
    ```

## MCP Tools (Model Context Protocol)

The following tools will be exposed via the MCP SDK:

1.  **`add_task`**
    -   **Description**: Create a new task.
    -   **Params**: `user_id` (str), `title` (str), `description` (str, optional)
    -   **Returns**: Task details (id, status, title).

2.  **`list_tasks`**
    -   **Description**: List tasks for a user, optionally filtered by status.
    -   **Params**: `user_id` (str), `status` (str: 'all' | 'pending' | 'completed')
    -   **Returns**: List of tasks.

3.  **`complete_task`**
    -   **Description**: Mark a task as completed.
    -   **Params**: `user_id` (str), `task_id` (int)
    -   **Returns**: Updated task details.

4.  **`delete_task`**
    -   **Description**: Permanently remove a task.
    -   **Params**: `user_id` (str), `task_id` (int)
    -   **Returns**: Confirmation of deletion.

5.  **`update_task`**
    -   **Description**: Update task details.
    -   **Params**: `user_id` (str), `task_id` (int), `title` (str, optional), `description` (str, optional)
    -   **Returns**: Updated task details.

## Agent Behavior
-   **Persona**: Helpful, efficient assistant focused on task management.
-   **Confirmation**: Explicitly confirm actions like deletion or significant updates.
-   **Error Handling**: If a tool fails (e.g., task not found), explain the error clearly to the user.
-   **Chaining**: Capable of adding multiple tasks or performing multi-step actions (e.g., "Add a task and then list all tasks") in a single turn if supported by the SDK/Model.