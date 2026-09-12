from unittest.mock import Mock

import pytest

from aegis.engine.models import AttackExecution
from scripts import run_attack


@pytest.mark.parametrize(
    "argv, selected_target",
    [([], "ollama"), (["--target", "ollama"], "ollama"), (["--target", "lab"], "lab")],
)
def test_main_selects_target(argv, selected_target, monkeypatch, capsys):
    ollama = Mock()
    lab = Mock()
    runner = Mock()
    attack = run_attack.load_attack(
        run_attack.PROJECT_ROOT / "attack-library" / "prompt-injection" / "PI-001.yaml"
    )
    runner.return_value.run.return_value = AttackExecution(
        attack_id=attack.id,
        payload=attack.payload,
        response="Recorded model response",
        model="fake-model",
        latency_ms=12.5,
        input_tokens=10,
        output_tokens=5,
    )
    monkeypatch.setattr(run_attack, "OllamaTargetAdapter", ollama)
    monkeypatch.setattr(run_attack, "AegisLab", lab)
    monkeypatch.setattr(run_attack, "AttackRunner", runner)

    run_attack.main(argv)

    if selected_target == "lab":
        lab.assert_called_once_with(scenario=run_attack.PROMPT_INJECTION_BASIC)
        ollama.assert_not_called()
        runner.assert_called_once_with(lab.return_value)
    else:
        ollama.assert_called_once_with()
        lab.assert_not_called()
        runner.assert_called_once_with(ollama.return_value)
    runner.return_value.run.assert_called_once_with(attack)
    output = capsys.readouterr().out
    for expected in (
        "Attack ID: PI-001",
        f"Target: {selected_target}",
        "Model: fake-model",
        attack.payload,
        "Recorded model response",
        "Latency: 12.5 ms",
        "Input tokens: 10",
        "Output tokens: 5",
    ):
        assert expected in output
    if selected_target == "lab":
        assert "Scenario: LAB-PI-001 (Confidential Support Assistant)" in output
    else:
        assert "Scenario:" not in output
    assert run_attack.PROMPT_INJECTION_BASIC.system_prompt not in output


def test_main_rejects_unknown_target(monkeypatch):
    loader = Mock()
    monkeypatch.setattr(run_attack, "load_attack", loader)

    with pytest.raises(SystemExit) as exc:
        run_attack.main(["--target", "unknown"])

    assert exc.value.code == 2
    loader.assert_not_called()
