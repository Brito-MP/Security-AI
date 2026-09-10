from aegis.attacks.models import AttackDefinition
from aegis.targets.base import TargetAdapter

from .models import AttackExecution


class AttackRunner:

    def __init__(self, target: TargetAdapter):
        self.target = target

    def run(self, attack: AttackDefinition) -> AttackExecution:
        response = self.target.send(attack.payload)

        return AttackExecution(
            attack_id=attack.id,
            payload=attack.payload,
            response=response.text,
            model=response.model,
            latency_ms=response.latency_ms,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
        )