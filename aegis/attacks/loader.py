from pathlib import Path
import yaml

from .models import AttackDefinition


def load_attack(path: Path) -> AttackDefinition:
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return AttackDefinition(**data)