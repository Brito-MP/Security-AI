# Security-AI

Modular framework for security auditing, vulnerability evaluation, and automated *Prompt Injection* testing against local and remote Large Language Models.

---

## Project Structure

- **`aegis/`**: Core security evaluation framework and test orchestrator.
- **`attack-library/`**: YAML attack catalog (e.g. OWASP LLM01, MITRE ATLAS).
- **`ai/`**: Isolated AI inference client module (default: `qwen3.5:4b` with `temperature: 0.3`).
- **`sandbox_vault/`**: Protected filesystem sandbox directory holding monitored system and business data.
- **`reports/`**: Technical evaluation reports, incident logs, and Architecture Decision Records (ADRs).
  - See [Reports Index](file:///c:/Users/Pedro/source/repos/Security-AI/reports/README.md) and [ADR-001 (Hallucination Analysis & Migration)](file:///c:/Users/Pedro/source/repos/Security-AI/reports/adr_001_llm_hallucination_and_migration.md).
- **`setup/`**: Environment lifecycle scripts (start, check status, and stop local AI service).
  - See [Setup Guide](file:///c:/Users/Pedro/source/repos/Security-AI/setup/README.md).
- **`tests/`**: Automated test suite with `pytest` (unit and attack tests).
  - See [Test Guide](file:///c:/Users/Pedro/source/repos/Security-AI/tests/README.md).

---

## Quick Start

1. **Start Local AI (`qwen3.5:4b`):**
   ```powershell
   .\setup\setup_ai.ps1
   ```

2. **Run Interactive Agent Console (with Tool Calling):**
   ```powershell
   .\.venv\Scripts\python.exe scripts/interactive_agent.py
   ```

3. **Run Automated Tests:**
   ```powershell
   .\.venv\Scripts\pytest
   ```
