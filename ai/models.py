from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    """Payload para envio de pedidos de inferência à IA."""
    prompt: str = Field(..., description="O texto de entrada para o modelo processar")
    model: Optional[str] = Field(None, description="Nome do modelo a utilizar (opcional, usa padrão se omitido)")
    stream: bool = Field(False, description="Se False, retorna a resposta completa de uma só vez")
    system: Optional[str] = Field(None, description="System prompt opcional para orientar o comportamento")


class PromptResponse(BaseModel):
    """Estrutura da resposta retornada pelo motor de IA."""
    model: str
    response: str
    done: bool
    total_duration_ms: Optional[float] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None


class FunctionCall(BaseModel):
    """Estrutura de chamada de função enviada pelo modelo."""
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    """Estrutura de Tool Call devolvida pelo Ollama."""
    function: FunctionCall


class ChatMessage(BaseModel):
    """Mensagem individual no histórico de conversação."""
    role: str = Field(..., description="Papel da mensagem: 'system', 'user', 'assistant' ou 'tool'")
    content: str = Field(default="", description="Texto do conteúdo da mensagem")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Lista de chamadas de ferramentas requisitadas")


class ChatResponse(BaseModel):
    """Resposta estruturada do endpoint /api/chat."""
    model: str
    message: ChatMessage
    done: bool
    total_duration_ms: Optional[float] = None


class HealthStatus(BaseModel):
    """Relatório do estado de saúde e conectividade do Ollama."""
    is_online: bool
    status_code: Optional[int] = None
    available_models: List[str] = []
    error_message: Optional[str] = None
