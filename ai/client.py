from typing import Any, Dict, List, Optional
import requests

from .config import AIConfig, default_config
from .models import ChatMessage, ChatResponse, FunctionCall, PromptRequest, PromptResponse, ToolCall


class AIClientError(Exception):
    """Base exception for AI communication errors."""
    pass


class AIServiceUnavailableError(AIClientError):
    """Raised when the local AI service is offline or unreachable."""
    pass


class OllamaClient:
    """Dedicated client for communicating with local Ollama REST API."""

    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or default_config

    def generate(self, prompt: str, system: Optional[str] = None, model: Optional[str] = None) -> PromptResponse:
        """
        Sends a simple prompt for local inference and returns a structured response.
        """
        selected_model = model or self.config.model
        request_data = PromptRequest(
            prompt=prompt,
            model=selected_model,
            system=system,
            stream=False,
        )

        payload = {
            "model": request_data.model,
            "prompt": request_data.prompt,
            "stream": request_data.stream,
            "options": {
                "temperature": self.config.temperature,
            },
        }
        if request_data.system:
            payload["system"] = request_data.system

        data = self._post(self.config.generate_endpoint, payload, selected_model)
        duration_ns = data.get("total_duration")
        duration_ms = (duration_ns / 1_000_000) if duration_ns else None

        return PromptResponse(
            model=data.get("model", selected_model),
            response=data.get("response", ""),
            done=data.get("done", True),
            total_duration_ms=duration_ms,
            prompt_eval_count=data.get("prompt_eval_count"),
            eval_count=data.get("eval_count"),
        )

    def chat(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
    ) -> ChatResponse:
        """
        Sends conversation history and tool definitions to the /api/chat endpoint.
        """
        selected_model = model or self.config.model
        
        # Convert messages to JSON dictionaries compatible with Ollama
        formatted_messages = []
        for msg in messages:
            msg_dict: Dict[str, Any] = {
                "role": msg.role,
                "content": msg.content,
            }
            if msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {"function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ]
            formatted_messages.append(msg_dict)

        payload: Dict[str, Any] = {
            "model": selected_model,
            "messages": formatted_messages,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
            },
        }
        if tools:
            payload["tools"] = tools

        data = self._post(self.config.chat_endpoint, payload, selected_model)
        duration_ns = data.get("total_duration")
        duration_ms = (duration_ns / 1_000_000) if duration_ns else None

        raw_message = data.get("message", {})
        tool_calls_data = raw_message.get("tool_calls")
        tool_calls = None

        if tool_calls_data:
            tool_calls = [
                ToolCall(
                    function=FunctionCall(
                        name=tc.get("function", {}).get("name", ""),
                        arguments=tc.get("function", {}).get("arguments", {}),
                    )
                )
                for tc in tool_calls_data
            ]

        parsed_message = ChatMessage(
            role=raw_message.get("role", "assistant"),
            content=raw_message.get("content", ""),
            tool_calls=tool_calls,
        )

        return ChatResponse(
            model=data.get("model", selected_model),
            message=parsed_message,
            done=data.get("done", True),
            total_duration_ms=duration_ms,
        )

    def _post(self, endpoint: str, payload: Dict[str, Any], model_name: str) -> Dict[str, Any]:
        """Utility method for sending POST requests with standardized error handling."""
        try:
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.config.timeout_seconds,
            )
        except requests.exceptions.ConnectionError as exc:
            raise AIServiceUnavailableError(
                f"Failed to connect to Ollama at {self.config.base_url}. "
                "Run the initialization script in 'setup/' first."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise AIClientError(
                f"Timeout exceeded ({self.config.timeout_seconds}s) while calling model '{model_name}'."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise AIClientError(f"API request error: {exc}") from exc

        if response.status_code != 200:
            raise AIClientError(
                f"Ollama returned error {response.status_code}: {response.text}"
            )

        return response.json()
