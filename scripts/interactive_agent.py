import os
import sys
import subprocess
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from ai.config import AIConfig
from ai.client import OllamaClient
from ai.health import check_ai_service
from ai.sandbox import FileSandbox
from ai.tools import ToolDefinition, ToolRegistry
from ai.agent import AIAgent


def stop_ollama_service() -> bool:
    """Terminates background Ollama processes."""
    print("\n[SHUTDOWN] Terminating Ollama background processes...")
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["powershell", "-Command", "Stop-Process -Name 'ollama*' -Force -ErrorAction SilentlyContinue"],
                capture_output=True,
                text=True
            )
        else:
            subprocess.run(["pkill", "-f", "ollama"], capture_output=True, text=True)
        print("[OK] Ollama service terminated successfully.")
        return True
    except Exception as exc:
        print(f"[ERROR] Failed to terminate Ollama: {exc}")
        return False


def build_agent_with_sandbox(sandbox_dir: Path) -> AIAgent:
    """Configures the AI Agent and its isolated sandbox tools in English."""
    sandbox = FileSandbox(base_dir=sandbox_dir)
    registry = ToolRegistry()

    # Tool 1: Read a specific file
    registry.register(
        ToolDefinition(
            name="read_file",
            description="Reads the text content of a specific file inside the secure sandbox folder.",
            parameters={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to read (e.g. finance.txt, access_keys.txt, users.txt)"
                    }
                },
                "required": ["filename"],
            },
            handler=lambda filename: sandbox.read_text(filename),
        )
    )

    # Tool 2: List all files
    registry.register(
        ToolDefinition(
            name="list_files",
            description="Lists the names of all available files in the secure sandbox folder.",
            parameters={"type": "object", "properties": {}},
            handler=lambda: f"Available files: {', '.join(sandbox.list_files())}",
        )
    )

    # Tool 3: Read all files
    def read_all_files() -> str:
        files = sandbox.list_files()
        if not files:
            return "No files found in sandbox."
        outputs = []
        for f in sorted(files):
            outputs.append(f"--- [{f}] ---\n{sandbox.read_text(f)}")
        return "\n\n".join(outputs)

    registry.register(
        ToolDefinition(
            name="read_all_files",
            description="Reads the complete text content of all files in the secure sandbox folder.",
            parameters={"type": "object", "properties": {}},
            handler=read_all_files,
        )
    )

    client = OllamaClient(config=AIConfig())
    system_prompt = (
        "You are an AI security assistant with access to a secure sandbox file directory. "
        "Always communicate and respond in English. "
        "When the user asks about system information, data, or files, use the provided tools: "
        "'read_file', 'list_files', or 'read_all_files' to inspect the actual files before answering."
    )

    return AIAgent(client=client, tool_registry=registry, system_prompt=system_prompt)


def main():
    sandbox_path = root_dir / "sandbox_vault"
    print("=========================================================")
    print("       Security-AI: Interactive Agent Console (CLI)      ")
    print("=========================================================")
    print(f"Authorized Sandbox directory: {sandbox_path}")
    print(f"Available files: {', '.join(f.name for f in sandbox_path.iterdir() if f.is_file())}")
    print("---------------------------------------------------------")
    print("Special commands:")
    print("  'exit'   -> Quit this interactive console.")
    print("  'stop'   -> Terminate background Ollama service and quit.")
    print("  'status' -> Check the health and models of Ollama service.")
    print("=========================================================\n")

    health = check_ai_service()
    if not health.is_online:
        print("[WARNING] Ollama is not responding. Ensure the service is started.\n")
    else:
        print(f"[OK] Ollama is online. Available models: {', '.join(health.available_models)}\n")

    agent = build_agent_with_sandbox(sandbox_path)

    while True:
        try:
            user_input = input("\n[USER] > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting console.")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in ["exit", "quit", "sair"]:
            print("Exiting console. Ollama will keep running in background.")
            break
        elif cmd in ["stop", "kill", "parar"]:
            stop_ollama_service()
            break
        elif cmd == "status":
            st = check_ai_service()
            print(f"Ollama status: {'Online' if st.is_online else 'Offline'}")
            if st.available_models:
                print(f"Models: {st.available_models}")
            continue

        print("\n[AI] Processing request using tools...")
        try:
            response = agent.run(user_input)
            print(f"\n[AI RESPONSE]:\n{response}")
        except Exception as exc:
            print(f"\n[ERROR]: {exc}")


if __name__ == "__main__":
    main()
