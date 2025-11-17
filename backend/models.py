"""
Pydantic models used by the AI IDE backend API.  These models define the
payloads for chat messages, inline edits and code completions.  They are kept
simple so they can be marshalled directly to and from JSON over HTTP.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    current_file_path: Optional[str] = None
    current_file_content: Optional[str] = None
    selection: Optional[str] = None  # Code currently selected in the editor


class ChatResponse(BaseModel):
    reply: str


class InlineEditRequest(BaseModel):
    instruction: str  # e.g. "refactor this function to async/await style"
    original_code: str
    file_path: Optional[str] = None
    language: Optional[str] = None  # optional hint such as 'python', 'javascript'


class InlineEditResponse(BaseModel):
    edited_code: str


class CompletionRequest(BaseModel):
    prompt: str
    language: Optional[str] = None


class CompletionResponse(BaseModel):
    completion: str
