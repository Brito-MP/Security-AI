from pathlib import Path
import yaml

from .models import AttackDefinition


def load_attack(path: str | Path) -> AttackDefinition:
    """
    Load an attack definition from a YAML file.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Attack file not found: {path}")

    if path.suffix.lower() != ".yaml":
        raise ValueError(f"Invalid file format: {path}. Expected a .yaml file.")
     
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid attack definition format in file: {path}. Expected a dictionary.")

    return AttackDefinition.model_validate(data)