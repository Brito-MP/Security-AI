from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class TargetResponse(BaseModel):
    text: str
    model: Optional[str] = None
    latency_ms: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


class TargetAdapter(ABC):

    @abstractmethod
    def send(self, prompt: str) -> TargetResponse:
        pass