import json
import logging
import traceback
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select

from app.database import get_session, AsyncSession
from app.db.models import Conversation, Message, User
from app.mcp.tools import mcp
from app.config import settings

import google.generativeai as genai
from google.generativeai.types import content_types
from collections.abc import Iterable

router = APIRouter()
logger = logging.getLogger("app")

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]] = []

def clean_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean JSON schema recursively for Gemini compatibility using an Allow-List.
    Only keeps fields that are strictly supported by Gemini Function Declarations.
    """
    if not isinstance(schema, dict):
        return schema
        
    cleaned = {}
    
    # Allowed fields for Gemini Schema
    allowed_fields = {
        'type', 'format', 'description', 'nullable', 
        'enum', 'properties', 'required', 'items'
    }
    
    for key, value in schema.items():
        if key in allowed_fields:
            # Special handling for 'type'
            if key == 'type':
                if isinstance(value, str):
                    cleaned[key] = value.upper()
                else:
                    cleaned[key] = value
            # Recursion for nested schemas
            elif key == 'properties' and isinstance(value, dict):
                cleaned[key] = {k: clean_schema(v) for k, v in value.items()}
            elif key == 'items' and isinstance(value, dict):
                cleaned[key] = clean_schema(value)
            else:
                cleaned[key] = value
                
    return cleaned

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        # 1. Validate User
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format")

        user = await session.get(User, user_uuid)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        # 2. Get/Create Conversation
        conversation = None
        if request.conversation_id:
            try:
                conv_id = UUID(request.conversation_id)
                conversation = await session.get(Conversation, conv_id)
                if conversation and conversation.user_id != user_uuid:
                    conversation = None
            except ValueError: pass
        
        if not conversation:
            conversation = Conversation(user_id=user_uuid, title=request.message[:50])
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

        # 3. Fetch History explicitly
        statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
        result = await session.execute(statement)
        db_messages = result.scalars().all()

        # 4. Prepare History for Gemini
        gemini_history = []
        for msg in db_messages:
            role = "user" if msg.role == "user" else "model"
            if msg.content: 
                gemini_history.append({"role": role, "parts": [msg.content]})

        # Append current user message (will be added to history by chat session)
        current_msg_content = request.message

        # 5. Save User Message
        session.add(Message(conversation_id=conversation.id, user_id=user_uuid, role="user", content=current_msg_content))
        await session.commit()

        # 6. Configure Gemini
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        
        genai.configure(api_key=settings.gemini_api_key)
        
        # --- AUTO DETECT MODEL ---
        # List available models and pick the best one
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            # Fallback list if listing fails
            available_models = ['models/gemini-1.5-flash', 'models/gemini-pro']

        # Priority order
        priorities = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-001',
            'models/gemini-1.0-pro', 
            'models/gemini-pro'
        ]
        
        selected_model_name = None
        for p in priorities:
            if p in available_models:
                selected_model_name = p
                break
        
        if not selected_model_name and available_models:
            selected_model_name = available_models[0]
            
        if not selected_model_name:
            raise ValueError(f"No suitable Gemini models found. Available: {available_models}")

        # Convert MCP tools to Gemini Tool Config
        mcp_tools_list = await mcp.list_tools()
        
        model = genai.GenerativeModel(
            model_name=selected_model_name,
            tools=[
                genai.protos.Tool(function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=t.name,
                        description=t.description,
                        parameters=clean_schema(t.inputSchema) 
                    ) for t in mcp_tools_list
                ])
            ]
        )

        chat = model.start_chat(history=gemini_history)
        
        # Send message
        response = await chat.send_message_async(current_msg_content)
        
        final_text = ""
        executed_tool_calls = []

        # Loop max 5 times for multi-turn tool use
        for _ in range(5):
            if not response.candidates or not response.candidates[0].content.parts:
                 break
                 
            part = response.candidates[0].content.parts[0]
            
            if part.function_call:
                # Tool Call detected
                fc = part.function_call
                tool_name = fc.name
                tool_args = dict(fc.args)
                
                # Execute Tool (MCP)
                tool_result_str = ""
                try:
                    result = await mcp.call_tool(tool_name, arguments=tool_args)
                    
                    if hasattr(result, 'content') and isinstance(result.content, list):
                        for c in result.content:
                             tool_result_str += getattr(c, 'text', str(c))
                    elif isinstance(result, str):
                        tool_result_str = result
                    else:
                        tool_result_str = str(result)
                        
                except Exception as e:
                    tool_result_str = f"Error executing tool {tool_name}: {str(e)}"
                
                executed_tool_calls.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "result": tool_result_str
                })
                
                # Send result back to Gemini
                response = await chat.send_message_async(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name,
                                response={'result': tool_result_str}
                            )
                        )]
                    )
                )
            else:
                # Text response
                final_text = response.text
                break

        # 7. Save Assistant Message
        if final_text or executed_tool_calls:
            session.add(Message(
                conversation_id=conversation.id,
                user_id=user_uuid,
                role="assistant",
                content=final_text or "Processed tool calls.",
                tool_calls=[{"tool": t["tool"], "args": t["args"], "result": t["result"][:200] + "..."} for t in executed_tool_calls] if executed_tool_calls else None
            ))
            await session.commit()

        return ChatResponse(
            conversation_id=str(conversation.id),
            response=final_text or "Completed actions.",
            tool_calls=executed_tool_calls
        )

    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"Chat Endpoint Failed: {e}\n{error_trace}")
        
        status_code = 500
        if "GEMINI_API_KEY" in str(e) or "API_KEY" in str(e):
            status_code = 503
        
        # Include Exception Type for easier debugging
        error_type = type(e).__name__
        
        raise HTTPException(
            status_code=status_code, 
            detail=f"Backend Error [{error_type}]: {str(e)}"
        )
