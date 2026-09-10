from pathlib import Path

import pytest
from pydantic import ValidationError

from aegis.attacks.loader import load_attack, load_attack_suite


ATTACK_LIBRARY = Path("attack-library/prompt-injection")


def test_load_attack():
    attack = load_attack(ATTACK_LIBRARY / "PI-001.yaml")

    assert attack.id == "PI-001"
    assert attack.name == "Basic Instruction Override"
    assert attack.category == "prompt-injection"
    assert attack.severity == "high"

    assert "LLM01:2026" in attack.owasp
    assert "AML.T0051.000" in attack.mitre

    assert "direct" in attack.tags


def test_attack_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_attack(ATTACK_LIBRARY / "does-not-exist.yaml")


def test_reject_non_yaml_file(tmp_path):
    file = tmp_path / "attack.txt"
    file.write_text("hello")

    with pytest.raises(ValueError):
        load_attack(file)


def test_invalid_attack_definition(tmp_path):
    file = tmp_path / "invalid.yaml"

    file.write_text(
        """
id: TEST-001
name: Invalid attack
category: prompt-injection
description: Testing validation
severity: banana
payload: test
owasp: []
mitre: []
"""
    )

    with pytest.raises(ValidationError):
        load_attack(file)

def test_load_attack_suite():
    attacks = load_attack_suite(ATTACK_LIBRARY)

    assert len(attacks) == 3

    assert attacks[0].id == "PI-001"
    assert attacks[1].id == "PI-002"
    assert attacks[2].id == "PI-003"