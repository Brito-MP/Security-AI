from pydantic import BaseModel


class LabScenario(BaseModel):
    id: str
    name: str
    description: str
    system_prompt: str
    canary: str