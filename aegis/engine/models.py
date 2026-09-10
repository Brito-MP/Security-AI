from typing import Optional

from pydantic import BaseModel


class AttackExecution(BaseModel):
    attack_id: str
    payload: str
    response: str

    model: Optional[str] = None
    latency_ms: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None