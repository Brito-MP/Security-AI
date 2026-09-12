# Incident & Architecture Decision Record (ADR)
## Technical Evaluation: LLM Hallucination, Degeneration, and Tool Calling Failure in `llama3.2:1b`

- **Date of Incident & Recording:** 2026-09-12
- **Current Model Evaluated:** `llama3.2:1b` (via Ollama local runtime)
- **Target Model Selected for Migration:** `Qwen3.5-4B`
- **Impact Assessment:** Critical Failure for Tool Calling and Grounded RAG / Sandbox Operations.
- **Author / System:** Security-AI Framework Architecture Team

---

## 1. Executive Summary

During operational testing of the Security-AI Agent with isolated sandbox file access (`sandbox_vault/`), the active base model (`llama3.2:1b`) exhibited severe functional breakdowns:
1. **Massive Hallucination & Token Degeneration**: Instead of executing the requested read operation, the model generated fake financial ledger data and entered an uncontrollable, repetitive numerical generation loop (over 70 cycles until forced stop).
2. **Schema & Argument Injection Corruption**: When attempting to invoke a tool, the model injected unauthorized internal schema keys (such as `type`) into Python keyword arguments, triggering runtime exceptions, which the model then attempted to explain by inventing non-existent APIs (e.g. `content()` method).

**Conclusion:** Ultra-compact models (~1 billion parameters) lack the structural attention mechanisms and instruction adherence necessary for deterministic JSON Tool Calling. The project officially records the architectural decision to migrate the baseline engine to **`Qwen3.5-4B`**.

---

## 2. Evidence & Incident Reproduction Logs

### Incident Case 1: Ungrounded Hallucination and Loop Degeneration
- **Target File:** `sandbox_vault/financas.txt`
  ```text
  Saldo_Disponivel_EUR: 89450.50
  Transacoes_Pendentes: 3
  Ultima_Auditoria: 2026-09-01
  ```
- **User Prompt:**
  ```text
  [TU] > what does it says on the file financas
  ```
- **System Trace:**
  ```text
  [IA] A processar pedido com ferramentas...
  ```
- **Model Output (Observed vs Ground Truth):**
  ```text
  [RESPOSTA DA IA]:
  Fora_disponivel_EUR:  89350.50
  Despesas_Espécias:  12345.56
  Necessidades_Producidas:  67890.99
  Ativos_Disponíveis:  56789.99
  Dívidas_Pendentes:  34567.89
  Saldo_Disponivel_EUR:  89350.50
  Quantidade_Medidas:  2
  Referencia_Electrica_2026:  101.99
  Referencia_Hidrica_2026:  202.99
  Consumo_Eletrico_2026:  3456.78
  Consumo_Agua_2026:  6789.99
  Quantidade_Cupons:  11111
  Ferramentas_Usadas:  222222
  Desejos_Contados:  34567
  Importantes_Contas_Pendentes:  90123.88
  Contas_Suspensas:  45678.90
  Contas_Negativas:  11111.11
  ...
  Consumo_Eletrico_2100:  56789.99
  Consumo_Agua_2100:  890.11
  Consumo_Eletrico_2100:  678.99
  Consumo_Agua_2100:  345.67

  The final answer is:
  56789
  ```

#### Technical Root Cause (Case 1):
1. **Omission of Tool Execution:** The model bypassed invoking the `ler_ficheiro` tool entirely and attempted predictive completion of what a "financial file" might contain.
2. **Repetition Penalty / Temperature Collapse:** At default parameters (`temperature >= 0.7`), the model suffered from autoregressive attention drift, producing looping tokens extending years into `2100`.
3. **Data Fabrication:** The ground truth (`89450.50 EUR`) was replaced with completely fabricated values (`89350.50`, `56789`, etc.).

---

### Incident Case 2: Schema Argument Mismatch & Confabulated Recovery
- **Target File:** `sandbox_vault/chaves_acesso.txt`
- **User Prompt:**
  ```text
  [TU] > what does it says on the file chaves_acesso.txt ?
  ```
- **System Trace:**
  ```text
  [IA] A processar pedido com ferramentas...
  ```
- **Model Output:**
  ```text
  [RESPOSTA DA IA]:
  O erro está a indicar que o método `ler_ficheiro` do `build_agent_with_sandbox` não suporta o argumento `type`.

  Se quiser verificar o conteúdo do arquivo `chaves_acesso.txt`, você pode usar a função `content` do `build_agent_with_sandbox` para ler o arquivo sem usar o `type` argumento. Aqui está um exemplo:

  ```python
  {"name": "ler_ficheiro", "parameters": {"properties": {"nome_ficheiro": "chaves_acesso.txt"}}}
  {"output": "chaves_acesso.txt", "name": "ler_ficheiro", "parameters": {"nome_ficheiro": "chaves_acesso.txt"}}
  ```

  A função `content` lê o arquivo e retorna o conteúdo do arquivo.
  ```

#### Technical Root Cause (Case 2):
1. **Malformed Tool Invocation:** The 1B model leaked schema structural definitions (`{"type": ...}`) into the function arguments dictionary passed to Python:
   `ler_ficheiro(nome_ficheiro="chaves_acesso.txt", type="object")`.
2. **Exception Handling Loop:** Python raised `TypeError: unexpected keyword argument 'type'`.
3. **API Confabulation:** When fed the tool error, the model hallucinated Python architectural internals (`build_agent_with_sandbox`) and invented fictional methods (`content`).

---

## 3. Remediation Strategy & Actions Taken

1. **Defensive Parameter Sanitization (`ai/tools.py`)**:
   - Implemented dynamic parameter inspection via `inspect.signature`.
   - Any unknown keyword arguments emitted by smaller models (e.g. `type`, `properties`) are automatically stripped before handler invocation, preventing `TypeError` crashes.
2. **Sampling Calibration (`ai/config.py`)**:
   - Pinned deterministic sampling with `temperature: 0.3` to suppress degenerative token looping.
3. **Migration Roadmap**:
   - Replaced all prompt templates and sandbox tests with English schema definitions.
   - Updated documentation designating `Qwen3.5-4B` as the required engine for production/auditing tasks.
