# Security-AI

Framework modular para auditoria de segurança, avaliação de vulnerabilidades e testes automatizados de *Prompt Injection* contra modelos de linguagem locais e remotos.

---

## Estrutura do Projeto

- **`aegis/`**: Núcleo do framework de segurança e orquestrador de testes.
- **`attack-library/`**: Catálogo de ataques em formato YAML (ex: OWASP LLM01, MITRE ATLAS).
- **`ai/`**: Módulo isolado de comunicação com o motor de inferência (Ollama local configurado com `temperature: 0.3`).
  - *Nota*: O modelo futuro padrão adotado pelo projeto é o **`Qwen3.5-4B`** (com suporte excelente para *Tool Calling* / *Function Calling*, leveza para CPU/iGPU/dGPU e prevenção de alucinações).
- **`setup/`**: Scripts de ciclo de vida do ambiente (iniciar, verificar estado e desligar a IA).
  - Consulta o [Guia de Setup](file:///c:/Users/Pedro/source/repos/Security-AI/setup/README.md).
- **`tests/`**: Suite de testes automatizados com `pytest` (unitários e ataques).
  - Consulta o [Guia de Execução dos Testes](file:///c:/Users/Pedro/source/repos/Security-AI/tests/README.md).

---

## Início Rápido

1. **Iniciar a IA local (`Qwen3.5-4B` / `llama3.2:1b`):**
   ```powershell
   .\setup\setup_ai.ps1
   ```

2. **Executar a consola interativa do agente (com leitura de ficheiros):**
   ```powershell
   .\.venv\Scripts\python.exe scripts/interactive_agent.py
   ```

3. **Executar os testes:**
   ```powershell
   .\.venv\Scripts\pytest
   ```
