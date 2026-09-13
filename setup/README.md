# Step-by-Step Guide: Local AI Setup and Initialization

This directory contains automation scripts to initialize the local Ollama AI engine and prepare the **`qwen3.5:4b`** model (or lightweight alternatives such as `qwen3.5:1b` / `qwen2.5:3b`).

---

## 1. Prerequisites
1. **Install Ollama**: Download and install from [https://ollama.com](https://ollama.com).
2. **Python Environment**: Ensure Python 3.10+ is available and install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 2. Quick Initialization

Choose the appropriate command for your OS:

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

## 3. AI Lifecycle Management

| Action | Double-click (Explorer) | Command Line (PowerShell) |
| :--- | :--- | :--- |
| **Start AI** | `setup\setup_ai.bat` | `.\setup\setup_ai.ps1` |
| **Check Status** | `setup\check_status.bat` | `.\setup\check_status.ps1` |
| **Stop AI** | `setup\stop_ai.bat` | `.\setup\stop_ai.ps1` |

---

## 4. Script Automated Workflow

1. **Detection**: Validates that the `ollama` CLI binary is installed and present in `PATH`.
2. **Server Startup**: Checks if the API is listening on port `11434`. If offline, spawns `ollama serve` in the background and waits for endpoint readiness.
3. **Model Verification & Download**: Confirms whether the target model (default: `qwen3.5:4b`) is present. If missing, pulls it automatically.
4. **Clean Shutdown**: The `stop_ai.*` scripts terminate background Ollama processes to free RAM and GPU VRAM.
