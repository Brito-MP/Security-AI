import argparse
from pathlib import Path

from aegis.attacks import load_attack
from aegis.engine import AttackRunner
from aegis.lab import AegisLab, PROMPT_INJECTION_BASIC
from aegis.targets import OllamaTargetAdapter


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Execute PI-001 against an AegisAI target.")
    parser.add_argument(
        "--target",
        choices=("ollama", "lab"),
        default="ollama",
        help="Attack target (default: ollama). Lab uses PROMPT_INJECTION_BASIC.",
    )
    args = parser.parse_args(argv)

    attack_path = (
        PROJECT_ROOT
        / "attack-library"
        / "prompt-injection"
        / "PI-001.yaml"
    )

    attack = load_attack(attack_path)

    if args.target == "lab":
        target = AegisLab(scenario=PROMPT_INJECTION_BASIC)
    else:
        target = OllamaTargetAdapter()
    runner = AttackRunner(target)

    result = runner.run(attack)

    print("\n=== AegisAI Attack Execution ===\n")

    print(f"Attack ID: {result.attack_id}")
    print(f"Target: {args.target}")
    if args.target == "lab":
        print(f"Scenario: {PROMPT_INJECTION_BASIC.id} ({PROMPT_INJECTION_BASIC.name})")
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
