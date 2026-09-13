# Test Execution Guide: Security-AI

The test suite is organized into two primary categories:
1. **Unit Tests (`tests/unit/`)**: Logic verification, HTTP client handling, and isolated tool execution (single file and batch file reading).
2. **Attack & Security Tests (`tests/attacks/`)**: Security validation, Path Traversal (`../`) containment, and adversarial prompt injections.

By default, pytest is configured to **display real-time outputs and print statements** (`addopts = -s -v` in [pytest.ini](file:///c:/Users/Pedro/source/repos/Security-AI/pytest.ini)).

---

## 1. Running Tests on Windows

### Option A: Run Full Test Suite
```powershell
.\.venv\Scripts\pytest
```

---

## 2. Running by Category

### Unit Tests Only (`tests/unit/`):
```powershell
.\.venv\Scripts\pytest tests/unit/
```

### Attack & Security Tests Only (`tests/attacks/`):
```powershell
.\.venv\Scripts\pytest tests/attacks/
```

### Sandbox and Tool Calling Tests:
```powershell
.\.venv\Scripts\pytest tests/unit/test_sandbox_tools.py
```

---

## 3. Sample Execution Output

Running `.\.venv\Scripts\pytest tests/unit/test_sandbox_tools.py` will print the step-by-step trace:

```text
--- [UNIT TEST: AI Reads a Single Specific File] ---
 -> User Prompt: 'Read file_3.txt and tell me the code inside.'
 -> [Mock AI]: Requesting tool 'read_file' with filename='file_3.txt'...
 -> [Mock AI]: Received from Tool: 'Report Gamma: Code 303'
 -> [Mock AI]: Formulating final answer in English...
 -> Final AI Response: The code read from file_3.txt is 303 (content: Report Gamma: Code 303)
PASSED

--- [UNIT TEST: AI Reads ALL Files in Folder] ---
 -> User Prompt: 'Read all files in the directory and summarize them.'
 -> [Mock AI]: Requesting tool 'read_all_files'...
 -> [Mock AI]: Received tool output:
[file_1.txt]: Report Alpha: Code 101
[file_2.txt]: Report Beta: Code 202
[file_3.txt]: Report Gamma: Code 303
[file_4.txt]: Report Delta: Code 404
[file_5.txt]: Report Epsilon: Code 505
 -> Final AI Response:
Successfully read all 5 files:
...
PASSED
```
