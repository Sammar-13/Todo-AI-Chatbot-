# Phase 3: Todo AI Chatbot - Constitution

## Vision Statement
To create an intelligent, stateless AI chatbot that empowers users to manage their tasks through natural language, leveraging the OpenAI Agents SDK and the Model Context Protocol (MCP) for robust, tool-driven interactions.

## Goals
1.  **AI Integration**: Implement a sophisticated agent using OpenAI Agents SDK that understands user intent regarding task management.
2.  **Tool-Use Architecture**: Expose core application logic (Todo CRUD) strictly via the Model Context Protocol (MCP).
3.  **Stateless Design**: Ensure the backend remains purely stateless, persisting all conversation and task data in a Neon PostgreSQL database.
4.  **Robust Persistence**: Guarantee that tasks, conversations, and individual messages are reliably stored and retrievable, allowing sessions to survive server restarts.
5.  **Seamless Frontend**: Integrate the chat experience into the existing application using a ChatKit-compatible UI.

## Non-Goals
-   **Voice Interface**: The initial phase focuses solely on text-based interaction.
-   **Multi-Modal Inputs**: Image or file analysis is out of scope for this phase.
-   **Complex Reasoning**: The agent is scoped to task management, not general-purpose assistance beyond this domain.

## Success Criteria
-   Users can add, list, complete, update, and delete tasks using natural language.
-   The system persists context across server restarts (conversations are saved).
-   The API adheres strictly to the `POST /api/{user_id}/chat` signature.
-   MCP tools are correctly invoked by the agent to perform actions.
-   The solution is deployed and functional on Vercel (or equivalent) with a live database.

## Constraints
-   **Strict Stack**: Must use OpenAI Agents SDK, Official MCP SDK, FastAPI, SQLModel, and Neon Postgres.
-   **No Local State**: No in-memory storage of conversation history between requests.
-   **Security**: All tool executions must be authorized for the specific user.