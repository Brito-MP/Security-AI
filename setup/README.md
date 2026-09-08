# Passo a Passo: Configuração e Arranque da IA Local

Este diretório contém os scripts de automação para inicializar o motor de inteligência artificial local com o **Ollama** e preparar o modelo **`llama3.2:1b`**.

---

## 1. Pré-Requisitos
1. **Instalar o Ollama**: Descarrega e instala a partir de [https://ollama.com](https://ollama.com).
2. **Ambiente Python**: Garante que tens Python 3.10+ e instala as dependências na raiz do projeto:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 2. Inicialização Rápida

Podes escolher o método de acordo com o teu sistema:

### Windows (PowerShell - Recomendado)
```powershell
.\setup\setup_ai.ps1
```
*Dica:* Para usar outro modelo no futuro, basta passar o parâmetro `-Model`:
```powershell
.\setup\setup_ai.ps1 -Model "phi3.5"
```

### Windows (Prompt de Comando / CMD)
```cmd
setup\setup_ai.bat
```

### Linux / macOS / WSL
```bash
chmod +x setup/setup_ai.sh
./setup/setup_ai.sh
```

---

## 3. Gestão do Ciclo de Vida da IA

| Ação | Duplo-clique (Windows Explorer) | Linha de Comandos (PowerShell) |
| :--- | :--- | :--- |
| **Iniciar IA** | `setup\setup_ai.bat` | `.\setup\setup_ai.ps1` |
| **Verificar Estado** | `setup\check_status.bat` | `.\setup\check_status.ps1` |
| **Desligar IA** | `setup\stop_ai.bat` | `.\setup\stop_ai.ps1` |

---

## 4. O que os scripts fazem automaticamente

1. **Deteção**: Validam se o binário `ollama` está instalado e acessível no `PATH`.
2. **Arranque do Servidor**: Verificam se o servidor já está a escutar na porta `11434`. Se não estiver, iniciam `ollama serve` em segundo plano e aguardam até o endpoint estar responsivo.
3. **Download do Modelo**: Verificam se o modelo `llama3.2:1b` já se encontra localmente. Se não estiver, executam automaticamente `ollama pull llama3.2:1b`.
4. **Encerramento Limpo**: O script `stop_ai.*` fecha os processos do Ollama libertando a memória RAM e VRAM da GPU.

