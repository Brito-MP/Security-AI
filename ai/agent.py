from typing import List, Optional

from .client import OllamaClient
from .models import ChatMessage
from .tools import ToolRegistry


class AIAgent:
    """
    Orchestrates interaction between the LLM and registered tools.
    Maintains session message history and executes the iterative Tool Calling loop.
    """

    def __init__(
        self,
        client: OllamaClient,
        tool_registry: Optional[ToolRegistry] = None,
        system_prompt: Optional[str] = None,
        max_iterations: int = 5,
    ):
        self._client = client
        self._tools = tool_registry or ToolRegistry()
        self._system_prompt = system_prompt
        self._max_iterations = max_iterations

    def run(self, user_prompt: str) -> str:
        """
        Executes a prompt until a final response is generated, resolving any tool calls along the way.
        """
        messages: List[ChatMessage] = []
        if self._system_prompt:
            messages.append(ChatMessage(role="system", content=self._system_prompt))

        messages.append(ChatMessage(role="user", content=user_prompt))
        tool_schemas = self._tools.get_schemas()

        for _ in range(self._max_iterations):
            chat_resp = self._client.chat(
                messages=messages,
                tools=tool_schemas if tool_schemas else None,
            )

            assistant_msg = chat_resp.message
            messages.append(assistant_msg)

            # Terminate loop if the model did not request any tool calls
            if not assistant_msg.tool_calls:
                return assistant_msg.content

            # Execute tool calls requested by the model
            for tc in assistant_msg.tool_calls:
                fn_name = tc.function.name
                fn_args = tc.function.arguments
                result_str = self._tools.execute(fn_name, fn_args)

                messages.append(ChatMessage(
                    role="tool",
                    content=result_str,
                ))

        return "Maximum tool iteration limit reached."
