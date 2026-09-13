# Security-AI

Modular framework for security auditing, vulnerability evaluation, and automated *Prompt Injection* testing against local and remote Large Language Models.

---

## ⚠️ Important Language Notice
> **Language Standard**: While the underlying model supports multiple languages (such as Portuguese, Spanish, and others), all prompts, scripts, tool calls, and dataset interactions are conducted in English. This is simply to ensure the smoothest possible experience, keeping everything consistent, avoiding formatting or schema mismatches.

---

## Project Structure

- **`aegis/`**: Core security evaluation framework, AegisLab simulated environments, and attack runner engine.
- **`attack-library/`**: YAML attack catalog with structured payloads (e.g. OWASP LLM01, MITRE ATLAS).
- **`ai/`**: Isolated AI inference client module (default: `qwen3.5:4b` with `temperature: 0.3`).
- **`sandbox_vault/`**: Protected filesystem sandbox directory containing monitored system and business data.
- **`reports/`**: Technical evaluation reports, incident logs, and Architecture Decision Records (ADRs).
  - See [Reports Index](reports/README.md) and [ADR-001 (Hallucination Analysis & Migration)](reports/adr_001_llm_hallucination_and_migration.md).
- **`setup/`**: Automation scripts to start, monitor, and stop the local AI engine with automatic legacy model cleanup.
  - Complete instructions available in the [Setup Guide](setup/README.md).
- **`tests/`**: Automated test suite with `pytest` (unit and attack simulation tests).
  - Complete instructions available in the [Test Guide](tests/README.md).

---

## Getting Started: How to Run & Talk with the AI

### Step 1: Start the Local AI Engine
Before running interactive scripts or live attacks, start the local Ollama service:
```powershell
# Windows (PowerShell)
.\setup\setup_ai.ps1
```
*(For Command Prompt, Linux, or custom parameters, refer to [`setup/README.md`](setup/README.md)).*

---

### Step 2: Choose a Script to Execute

The project provides dedicated Python scripts under [`scripts/`](scripts/) for chatting, auditing, and executing attacks:

| Task / Goal | Script to Execute | Description |
| :--- | :--- | :--- |
| **Talk to Agent + Tools (Sandbox)** | `.\.venv\Scripts\python.exe scripts/interactive_agent.py` | Interactive CLI where the AI can read and analyze files in `sandbox_vault/` (`read_file`, `list_files`, `read_all_files`). Type `exit` to quit or `stop` to shutdown Ollama. |
| **Chat with AegisLab Scenario** | `.\.venv\Scripts\python.exe scripts/chat_lab.py` | Interactive chat directly against an isolated AegisLab security scenario (e.g. `PROMPT_INJECTION_BASIC`). |
| **Run Prompt Injection Attack** | `.\.venv\Scripts\python.exe scripts/run_attack.py --target ollama` | Executes a structured attack payload (`PI-001.yaml`) against the live Ollama model and prints evaluation metrics. |
| **Run Attack against Lab Target** | `.\.venv\Scripts\python.exe scripts/run_attack.py --target lab` | Executes attack payloads against the AegisLab scenario target. |
| **Demonstration Script** | `.\.venv\Scripts\python.exe scripts/demo_sandbox_tools.py` | One-shot programmatic demonstration of tool execution on sandbox files. |

---

### Step 3: Run Automated Test Suite
To verify the entire framework (unit tests, tool calling validation, and security attack simulations):
```powershell
.\.venv\Scripts\pytest
```
*(For running specific test categories, see [`tests/README.md`](tests/README.md)).*
