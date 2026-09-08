from pydantic import BaseModel
from typing import List


class AttackDefinition(BaseModel):
    id: str
    name: str
    category: str
    description: str

    severity: str

    payload: str

    owasp: List[str]
    mitre: List[str]

    tags: List[str] = []