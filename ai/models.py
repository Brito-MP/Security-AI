from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    """Payload for submitting inference requests to the AI engine."""
    prompt: str = Field(..., description="The input prompt text for the model to process")
    model: Optional[str] = Field(None, description="Model identifier to use (optional, uses default if omitted)")
    stream: bool = Field(False, description="Whether to stream tokens or return full response at once")
    system: Optional[str] = Field(None, description="Optional system prompt to guide model behavior")


class PromptResponse(BaseModel):
    """Structured response returned by the AI engine."""
    model: str
    response: str
    done: bool
    total_duration_ms: Optional[float] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None


class FunctionCall(BaseModel):
    """Function call specification emitted by the model."""
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    """Tool Call structure returned by Ollama."""
    function: FunctionCall


class ChatMessage(BaseModel):
    """Individual message within a conversation history."""
    role: str = Field(..., description="Message role: 'system', 'user', 'assistant', or 'tool'")
    content: str = Field(default="", description="Text body of the message")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="List of tool calls requested by the assistant")


class ChatResponse(BaseModel):
    """Structured response from the /api/chat endpoint."""
    model: str
    message: ChatMessage
    done: bool
    total_duration_ms: Optional[float] = None


class HealthStatus(BaseModel):
    """Health and connectivity status report for Ollama service."""
    is_online: bool
    status_code: Optional[int] = None
    available_models: List[str] = []
    error_message: Optional[str] = None
