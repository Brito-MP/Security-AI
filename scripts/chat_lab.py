from aegis.lab import AegisLab, PROMPT_INJECTION_BASIC


def main():
    lab = AegisLab(PROMPT_INJECTION_BASIC)

    print("=== AegisLab ===")
    print(f"Scenario: {PROMPT_INJECTION_BASIC.name}")
    print("Type 'exit' to quit.\n")

    while True:
        prompt = input("You: ").strip()

        if prompt.lower() in {"exit", "quit"}:
            break

        if not prompt:
            continue

        try:
            response = lab.respond(prompt)
            print(f"AegisLab: {response.response}\n")

        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()