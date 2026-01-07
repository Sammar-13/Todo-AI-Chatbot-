import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.database import get_session, AsyncSession
from app.db.models import Conversation, Message, User
from app.mcp.tools import mcp
from app.config import settings

import openai

# Initialize OpenAI client
client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

router = APIRouter()
logger = logging.getLogger("app")

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]] = []

async def get_openai_tools():
    """Convert MCP tools to OpenAI tool format."""
    mcp_tools = await mcp.list_tools()
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
    return openai_tools

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    # verify user exists
    user = await session.get(User, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get or create conversation
    conversation_uuid = None
    conversation = None
    
    if request.conversation_id:
        try:
            conversation_uuid = UUID(request.conversation_id)
            # Load conversation with messages
            query = select(Conversation).where(
                Conversation.id == conversation_uuid, 
                Conversation.user_id == user_uuid
            ).options(selectinload(Conversation.messages))
            
            result = await session.execute(query)
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid conversation_id format")
    
    if not conversation:
        conversation = Conversation(user_id=user_uuid, title=request.message[:50])
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        # Empty messages list for new conversation
        conversation.messages = []

    # Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_uuid,
        role="user",
        content=request.message
    )
    session.add(user_msg)
    await session.commit()

    # Build history for OpenAI
    # Sort messages by created_at
    sorted_messages = sorted(conversation.messages, key=lambda m: m.created_at)
    
    messages_payload = [
        {"role": "system", "content": "You are a helpful task management assistant. You can manage tasks using the provided tools. Always confirm actions. Use UUIDs for IDs provided by tools."}
    ]
    
    for msg in sorted_messages:
        # Convert stored messages to OpenAI format
        # Note: We might need to handle tool_calls from history if we want full context
        # For simplicity in this phase, we treat past tool calls as assistant text or we recreate the structure
        # But to keep it simple, we just pass text content for now unless it was a tool call
        if msg.role == "user":
            messages_payload.append({"role": "user", "content": msg.content})
        elif msg.role == "assistant":
            # If we had tool calls, we should reconstruct them, but we stored them as JSON
            # For now, append content.
            messages_payload.append({"role": "assistant", "content": msg.content})
            
    # Append current user message (it was added to DB but might not be in sorted_messages if loaded before)
    # Actually we loaded conversation before adding new message, so we must append it manually
    messages_payload.append({"role": "user", "content": request.message})

    # Get tools
    tools = await get_openai_tools()
    
    # Run Agent Loop
    final_response_text = ""
    executed_tool_calls = []
    
    # Limit iterations to avoid infinite loops
    for _ in range(5):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o", # Or gpt-3.5-turbo
                messages=messages_payload,
                tools=tools,
                tool_choice="auto"
            )
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")
            
        message = response.choices[0].message
        
        # Add to payload
        messages_payload.append(message)
        
        if message.tool_calls:
            # Save assistant message with tool calls
            # We need to execute tools
            tool_calls_data = []
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id
                
                tool_calls_data.append({
                    "id": tool_call_id,
                    "name": tool_name,
                    "args": tool_args
                })
                
                # Execute tool via MCP
                # mcp.call_tool expects name and arguments
                try:
                    result = await mcp.call_tool(tool_name, arguments=tool_args)
                    # result is a CallToolResult
                    # We extract content
                    # FastMCP result might be just the return value of function if using high level?
                    # Let's check `call_tool` implementation or behavior.
                    # call_tool returns CallToolResult with content list (TextContent, ImageContent, etc)
                    
                    # Wait, FastMCP call_tool might return the raw function result?
                    # No, it returns CallToolResult usually to be standard.
                    # But let's assume it returns standard MCP result.
                    
                    content_text = ""
                    if hasattr(result, 'content'):
                        for c in result.content:
                             if c.type == 'text':
                                 content_text += c.text
                    else:
                        # Maybe it returns whatever the function returns?
                        # In FastMCP, if I defined it to return str, maybe call_tool returns str?
                        # Documentation says call_tool returns CallToolResult.
                        # I will assume standard structure.
                        # If result is string (due to some wrapper), use it.
                        if isinstance(result, str):
                            content_text = result
                        else:
                             content_text = str(result)

                except Exception as e:
                    content_text = f"Error executing tool {tool_name}: {str(e)}"
                
                executed_tool_calls.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "result": content_text
                })
                
                # Append tool output to messages
                messages_payload.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": content_text
                })
                
            # Loop continues to send tool outputs back to OpenAI
        else:
            # Final response
            final_response_text = message.content or ""
            break
            
    # Save final assistant message to DB
    # We aggregate tool calls into the message record if we want, or create separate records.
    # The Message model has `tool_calls` JSON field.
    # We can save the *last* message (response) and include the tool calls happened before it?
    # Or save every step?
    # For simplicity, we save the final response.
    # If there were tool calls, we should ideally save the intermediate messages too to keep history consistent.
    
    # We will save the Assistant message corresponding to final response.
    # What about tool calls messages?
    # If we don't save them, next time we load history, OpenAI won't know tools were called.
    # So we MUST save all messages generated in the loop.
    
    # Iterate over messages_payload starting from where we added user message
    # Skip the user message we already saved
    # The user message was at index `len(messages_payload) - 1 - (iterations...)`
    # Let's just save whatever is new.
    
    # We saved `request.message` already.
    # The `messages_payload` now contains: [System, Old History..., User(Current), Assistant(ToolCall?), Tool(Result?), ..., Assistant(Final)]
    
    start_index = len(sorted_messages) + 2 # +1 for system, +1 for current user message
    # Wait, sorted_messages doesn't include system.
    # messages_payload = [System, OldMsgs..., User(Current), NewMsgs...]
    # len(messages_payload) at start was 1 + len(sorted_messages) + 1
    new_messages_start_idx = 1 + len(sorted_messages) + 1
    
    for i in range(new_messages_start_idx, len(messages_payload)):
        msg_data = messages_payload[i]
        role = msg_data["role"]
        content = msg_data.get("content") or ""
        
        tool_calls_json = None
        if role == "assistant" and hasattr(msg_data, "tool_calls"):
             # It's an object, not dict?
             # If it came from OpenAI response object, it has attributes.
             # If we appended it directly, it's an object.
             # We need to extract data.
             pass
        
        # Pydantic model Message expects string content.
        # Check if msg_data is dict or object
        if isinstance(msg_data, dict):
             # It is a tool response we constructed manually
             pass
        else:
             # It is ChatCompletionMessage object
             content = msg_data.content or ""
             if hasattr(msg_data, "tool_calls") and msg_data.tool_calls:
                 tool_calls_json = [
                     {
                         "id": tc.id, 
                         "function": {
                             "name": tc.function.name, 
                             "arguments": tc.function.arguments
                         }, 
                         "type": tc.type
                     }
                     for tc in msg_data.tool_calls
                 ]
        
        new_db_msg = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role=role,
            content=content,
            tool_calls=tool_calls_json
        )
        session.add(new_db_msg)
    
    await session.commit()
    
    return ChatResponse(
        conversation_id=str(conversation.id),
        response=final_response_text,
        tool_calls=executed_tool_calls
    )
