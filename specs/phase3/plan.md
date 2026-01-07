# Phase 3: Todo AI Chatbot - Implementation Plan

## Phase Overview
This phase integrates an AI chatbot into the existing application. The backend will be enhanced with an OpenAI Agent and an MCP server, while the frontend will receive a new chat interface.

## Step 1: Backend Infrastructure & Database
**Goal**: Prepare the database and backend structure for chat persistence.
1.  Install necessary dependencies: `openai-agents-sdk`, `mcp`, `asyncpg` (if not present).
2.  Define `Conversation` and `Message` SQLModel classes.
3.  Create and run Alembic migrations to add these tables.
4.  Verify `Task` model compatibility.

## Step 2: MCP Server & Tool Implementation
**Goal**: Encapsulate business logic into MCP tools.
1.  Set up the MCP Server instance within the FastAPI app.
2.  Implement `add_task` tool function and register it.
3.  Implement `list_tasks` tool function and register it.
4.  Implement `complete_task` tool function and register it.
5.  Implement `delete_task` tool function and register it.
6.  Implement `update_task` tool function and register it.
7.  Verify tools can be called programmatically (unit test).

## Step 3: OpenAI Agent & Chat Endpoint
**Goal**: Connect the Agent to the MCP tools and expose the chat API.
1.  Create the `POST /api/{user_id}/chat` endpoint.
2.  Implement logic to fetch conversation history from DB.
3.  Initialize the OpenAI Agent (using `gpt-4o` or compatible model) with the MCP tool definitions.
4.  Execute the agent with the user's message.
5.  Capture the agent's response and tool calls.
6.  Persist the new message exchange to the DB.
7.  Return the response to the client.

## Step 4: Frontend Chat Interface
**Goal**: Provide a user interface for the chatbot.
1.  Create a `ChatInterface` component in the frontend.
2.  Implement message history display (user vs. assistant bubbles).
3.  Implement an input area for sending messages.
4.  Connect the component to the backend `/api/{user_id}/chat` endpoint.
5.  Handle loading states (typing indicators).
6.  Display tool call results (optional, debug/transparency mode).

## Step 5: Integration & Verification
**Goal**: Ensure end-to-end functionality.
1.  Test the full flow: User sends "Buy milk" -> Agent calls `add_task` -> Task appears in DB -> Agent replies "Added task 'Buy milk'".
2.  Verify state persistence: Restart backend -> Reload chat -> History remains.
3.  Deploy to Vercel/Neon and verify production functionality.