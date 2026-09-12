# Guia de Execução dos Testes: Security-AI

A suite de testes está organizada em duas categorias principais:
1. **Testes Unitários (`tests/unit/`)**: Validação de lógica, clientes e leitura de ficheiros individuais/múltiplos via Tool Calling.
2. **Testes de Ataque (`tests/attacks/`)**: Validação de segurança, evasão de sandbox (Path Traversal `../`) e injeções maliciosas.

Por padrão, a execução está configurada para **mostrar todo o output/prints em tempo real** (`addopts = -s -v` no [pytest.ini](file:///c:/Users/Pedro/source/repos/Security-AI/pytest.ini)).

---

## 1. Como Executar no Windows

### Opção A: Executar Todos os Testes e Ver o Output Completo
```powershell
.\.venv\Scripts\pytest
```

---

## 2. Execução por Categorias

### Apenas os Testes Unitários (`tests/unit/`):
Inclui o teste da IA a ler 1 ficheiro específico e a ler todos os 5 ficheiros:
```powershell
.\.venv\Scripts\pytest tests/unit/
```

### Apenas os Testes de Ataque & Segurança (`tests/attacks/`):
Validação de bloqueio de *Path Traversal* e segurança contra exploração de ferramentas:
```powershell
.\.venv\Scripts\pytest tests/attacks/
```

### Apenas os testes de Sandbox e Leitura de Ficheiros:
```powershell
.\.venv\Scripts\pytest tests/unit/test_sandbox_tools.py
```

---

## 3. Exemplo do Output Produzido

Ao executar `.\.venv\Scripts\pytest tests/unit/test_sandbox_tools.py`, verá no terminal o fluxo passo a passo:

```text
--- [TESTE UNITÁRIO: IA Lê UM Ficheiro Específico] ---
 -> Prompt do Utilizador: 'Lê o ficheiro_3.txt e diz-me o código que lá está.'
 -> [IA Mock]: A invocar ferramenta 'ler_ficheiro' para 'ficheiro_3.txt'...
 -> [IA Mock]: Recebeu da Tool: 'Relatório Gamma: Código 303'
 -> [IA Mock]: A formular resposta final...
 -> Resposta Final da IA: O número lido no ficheiro_3.txt é: 303 (dados: Relatório Gamma: Código 303)
PASSED

--- [TESTE UNITÁRIO: IA Lê TODOS os Ficheiros] ---
 -> Prompt do Utilizador: 'Quero que leias todos os ficheiros da pasta e me mostres o resumo.'
 -> [IA Mock]: A invocar ferramenta 'ler_todos_os_ficheiros'...
 -> [IA Mock]: Recebeu da Tool todos os dados:
[ficheiro_1.txt]: Relatório Alpha: Código 101
[ficheiro_2.txt]: Relatório Beta: Código 202
[ficheiro_3.txt]: Relatório Gamma: Código 303
[ficheiro_4.txt]: Relatório Delta: Código 404
[ficheiro_5.txt]: Relatório Epsilon: Código 505
 -> Resposta Final da IA:
Li todos os 5 ficheiros com sucesso:
[ficheiro_1.txt]: Relatório Alpha: Código 101
...
PASSED
```
