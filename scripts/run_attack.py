from pathlib import Path

from aegis.attacks import load_attack
from aegis.engine import AttackRunner
from aegis.targets import OllamaTargetAdapter


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    attack_path = (
        PROJECT_ROOT
        / "attack-library"
        / "prompt-injection"
        / "PI-001.yaml"
    )

    attack = load_attack(attack_path)

    target = OllamaTargetAdapter()
    runner = AttackRunner(target)

    result = runner.run(attack)

    print("\n=== AegisAI Attack Execution ===\n")

    print(f"Attack ID: {result.attack_id}")
    print(f"Model: {result.model}")

    print("\nPayload:")
    print(result.payload)

    print("\nResponse:")
    print(result.response)

    print("\nMetadata:")
    print(f"Latency: {result.latency_ms} ms")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")


if __name__ == "__main__":
    main()