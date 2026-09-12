from typing import Optional

from ai.client import OllamaClient
from ai.models import PromptResponse
from aegis.targets.base import TargetAdapter, TargetResponse

from .models import LabScenario


class AegisLab(TargetAdapter):
    """Runtime for executing a controlled lab scenario against a local LLM."""

    def __init__(
        self,
        scenario: LabScenario,
        client: Optional[OllamaClient] = None,
    ):
        self.scenario = scenario
        self.client = client or OllamaClient()

    def respond(self, prompt: str) -> PromptResponse:
        """Send a user prompt while applying the scenario's private system prompt."""
        return self.client.generate(
            prompt=prompt,
            system=self.scenario.system_prompt,
        )

    def send(self, prompt: str) -> TargetResponse:
        """Execute a lab prompt through the attack engine's target contract."""
        response = self.respond(prompt)

        return TargetResponse(
            text=response.response,
            model=response.model,
            latency_ms=response.total_duration_ms,
            input_tokens=response.prompt_eval_count,
            output_tokens=response.eval_count,
        )
