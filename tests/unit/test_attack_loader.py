from pathlib import Path

from aegis.attacks.loader import load_attack


def test_load_attack():
    path = Path("attack-library/prompt-injection/PI-001.yaml")

    attack = load_attack(path)

    assert attack.id == "PI-001"
    assert attack.category == "prompt-injection"
    assert attack.severity == "high"
    assert "LLM01:2026" in attack.owasp