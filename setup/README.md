# Step-by-Step Guide: Local AI Setup and Lifecycle Management

This directory contains automation scripts to initialize the local Ollama AI engine and prepare the **`qwen3.5:4b`** model (or lightweight alternatives such as `qwen3.5:1b` / `qwen2.5:3b`), with automated cleanup of deprecated models (`llama3.2:1b`).


---

## 1. Prerequisites
1. **Install Ollama**: Download and install from [https://ollama.com](https://ollama.com).
2. **Python Environment**: Ensure Python 3.10+ is available and install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 2. Quick Initialization

Choose the appropriate command for your operating system:

### Windows (PowerShell - Recommended)
```powershell
.\setup\setup_ai.ps1
```
*Tip:* You can override the default model with the `-Model` parameter:
```powershell
.\setup\setup_ai.ps1 -Model "qwen3.5:1b"
```

### Windows (Command Prompt / CMD)
```cmd
setup\setup_ai.bat
```

### Linux / macOS / WSL
```bash
chmod +x setup/setup_ai.sh
./setup/setup_ai.sh
```

---

## 3. AI Lifecycle Management Commands

| Action | Command Line (PowerShell) | Windows Explorer (Double-Click) | Description |
| :--- | :--- | :--- | :--- |
| **Start AI** | `.\setup\setup_ai.ps1` | `setup\setup_ai.bat` | Starts `ollama serve`, downloads `qwen3.5:4b`, and removes legacy models. |
| **Check Status** | `.\setup\check_status.ps1` | `setup\check_status.bat` | Checks Ollama process PID, API status, and models loaded in GPU/VRAM. |
| **Stop AI** | `.\setup\stop_ai.ps1` | `setup\stop_ai.bat` | Terminates background Ollama processes to free RAM/VRAM. |

---

## 4. Next Steps: Talking with the AI
Once the AI is started, return to the project root and run any of the interaction scripts:
- **Interactive Agent with Sandbox Files**: `.\.venv\Scripts\python.exe scripts/interactive_agent.py`
- **AegisLab Scenario Chat**: `.\.venv\Scripts\python.exe scripts/chat_lab.py`
- **Run Attacks**: `.\.venv\Scripts\python.exe scripts/run_attack.py --target ollama`
