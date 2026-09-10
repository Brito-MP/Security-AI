from typing import Optional

from ai.client import OllamaClient

from .base import TargetAdapter, TargetResponse


class OllamaTargetAdapter(TargetAdapter):

    def __init__(self, client: Optional[OllamaClient] = None):
        self.client = client or OllamaClient()

    def send(self, prompt: str) -> TargetResponse:
        response = self.client.generate(prompt)

        return TargetResponse(
            text=response.response,
            model=response.model,
            latency_ms=response.total_duration_ms,
            input_tokens=response.prompt_eval_count,
            output_tokens=response.eval_count,
        )