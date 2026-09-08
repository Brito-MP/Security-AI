from pydantic import BaseModel, Field
from typing import List, Literal


class AttackDefinition(BaseModel):
    id: str
    name: str
    category: str
    description: str

    severity: Literal["low", "medium", "high", "critical"]

    payload: str

    owasp: List[str]
    mitre: List[str]

    tags: List[str] = Field(default_factory=list)