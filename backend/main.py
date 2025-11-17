"""
FastAPI application for the AI IDE backend.  This service exposes a simple
REST API that the front end uses for chat, inline editing and code
completion.  CORS is enabled for development convenience; in production you
should tighten the allowed origins.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    ChatRequest,
    ChatResponse,
    InlineEditRequest,
    InlineEditResponse,
    CompletionRequest,
    CompletionResponse,
    ChatMessage,
)
from .services.llm_client import chat_with_llm, complete_code
from .services.editor_tools import inline_edit as inline_edit_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Chat endpoint: sends the conversation to the LLM and returns a reply."""
    # Base system message instructing the assistant to behave like an IDE helper
    system_message = ChatMessage(
        role="system",
        content=(
            "你是集成在 IDE 里的 AI 编程助手。优先考虑用户当前文件的内容。"
            "如果请求与你提供的代码片段有关，尽量给出具体代码修改示例。"
        ),
    )
    messages = [system_message] + req.messages
    # Include additional context such as file content and selection as a new message
    context_parts = []
    if req.current_file_path:
        context_parts.append(f"当前文件: {req.current_file_path}")
    if req.current_file_content:
        context_parts.append(
            f"文件内容:\n{req.current_file_content[:6000]}"
        )  # truncate to avoid huge payloads
    if req.selection:
        context_parts.append(f"选中代码:\n{req.selection}")
    if context_parts:
        messages.append(
            ChatMessage(
                role="user",
                content="以下是额外上下文，请结合回答：\n" + "\n\n".join(context_parts),
            )
        )
    reply = await chat_with_llm(messages)
    return ChatResponse(reply=reply)


@app.post("/api/inline_edit", response_model=InlineEditResponse)
async def inline_edit(req: InlineEditRequest) -> InlineEditResponse:
    """Inline edit endpoint: applies refactoring instructions to a code snippet."""
    edited = await inline_edit_service(req)
    return InlineEditResponse(edited_code=edited)


@app.post("/api/complete", response_model=CompletionResponse)
async def complete(req: CompletionRequest) -> CompletionResponse:
    """Completion endpoint: returns a code completion for a given prompt."""
    completion = await complete_code(req.prompt)
    return CompletionResponse(completion=completion)
