# Guia de Execução dos Testes: Security-AI

Este diretório contém a suite de testes automatizados do projeto (testes unitários e de integração).

---

## 1. Como Executar no Windows

### Opção A: Com o ambiente virtual ativado (Recomendado)

1. **Ativar o `.venv` no PowerShell:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(No CMD clássico usa: `.\.venv\Scripts\activate.bat`)*

2. **Executar os testes:**
   ```powershell
   pytest
   ```

---

### Opção B: Execução direta pelo executável do `.venv` (Sem ativar)

Podes correr diretamente sem precisar de ativar o ambiente:

- **PowerShell:**
  ```powershell
  .\.venv\Scripts\python.exe -m pytest -v
  ```

- **CMD (Prompt de Comando):**
  ```cmd
  .venv\Scripts\python.exe -m pytest -v
  ```

---

## 2. Como Executar no Linux / WSL / macOS

1. **Criar e ativar o ambiente virtual (se ainda não o fizeste):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Executar todos os testes:**
   ```bash
   pytest -v
   ```

3. **Ou execução direta (sem ativar):**
   ```bash
   ./.venv/bin/python -m pytest -v
   ```

---

## 3. Executar Testes Específicos

Podes filtrar e rodar apenas o que te interessa:

### Apenas os testes do motor de IA:
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\pytest tests/unit/test_ai_health.py tests/unit/test_ai_client.py -v
  ```
- **Linux / WSL:**
  ```bash
  pytest tests/unit/test_ai_health.py tests/unit/test_ai_client.py -v
  ```

### Apenas os testes do carregador de ataques (`attack-library`):
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\pytest tests/unit/test_attack_loader.py -v
  ```
- **Linux / WSL:**
  ```bash
  pytest tests/unit/test_attack_loader.py -v
  ```

### Apenas uma função de teste específica:
```powershell
pytest tests/unit/test_attack_loader.py -k "test_load_attack" -v
```

---

## 4. Teste ao Vivo com a IA Local (Inferência Real)

Para validar a comunicação real com o servidor Ollama e o modelo `llama3.2:1b` ativo:

- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\python.exe -c "from ai import check_ai_service, OllamaClient; print(check_ai_service()); print(OllamaClient().generate('Diz apenas: OK').response.strip())"
  ```

- **Linux / WSL:**
  ```bash
  ./.venv/bin/python -c "from ai import check_ai_service, OllamaClient; print(check_ai_service()); print(OllamaClient().generate('Diz apenas: OK').response.strip())"
  ```

---

## 5. Dicas Úteis do `pytest`

| Comando / Flag | Descrição |
| :--- | :--- |
| `pytest -v` | Modo verboso (mostra o nome de cada teste individualmente). |
| `pytest -s` | Mostra os `print()` no terminal durante a execução dos testes. |
| `pytest -x` | Interrompe a execução imediatamente no primeiro teste que falhar. |
| `pytest -k "palavra"` | Executa apenas os testes cujo nome contenha a palavra indicada. |
| `pytest --tb=short` | Resumo mais curto e limpo em caso de erros de asserção. |
