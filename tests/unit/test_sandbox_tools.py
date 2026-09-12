from pathlib import Path
import pytest

from ai.sandbox import FileSandbox, SandboxSecurityError
from ai.tools import ToolDefinition, ToolRegistry
from ai.agent import AIAgent
from ai.models import ChatMessage, ChatResponse, FunctionCall, ToolCall


@pytest.fixture
def sandbox_with_five_files(tmp_path: Path) -> FileSandbox:
    """Creates a sandbox with 5 distinct files containing phrases and codes in English."""
    sandbox = FileSandbox(base_dir=tmp_path / "sandbox")
    files = {
        "file_1.txt": "Report Alpha: Code 101",
        "file_2.txt": "Report Beta: Code 202",
        "file_3.txt": "Report Gamma: Code 303",
        "file_4.txt": "Report Delta: Code 404",
        "file_5.txt": "Report Epsilon: Code 505",
    }
    for filename, content in files.items():
        sandbox.write_text(filename, content)
    return sandbox


def test_sandbox_read_and_write(tmp_path: Path):
    print("\n--- [UNIT TEST: Read & Write Sandbox Operations] ---")
    sandbox = FileSandbox(base_dir=tmp_path)
    sandbox.write_text("doc1.txt", "sample test content 1")
    
    content = sandbox.read_text("doc1.txt")
    files = sandbox.list_files()
    
    print(f" -> Content read: '{content}'")
    print(f" -> Existing files: {files}")
    
    assert content == "sample test content 1"
    assert "doc1.txt" in files


def test_agent_read_single_file_tool(sandbox_with_five_files: FileSandbox):
    """
    Tests requesting the AI to read specifically ONE single file (e.g. file_3.txt).
    """
    print("\n--- [UNIT TEST: AI Reads a Single Specific File] ---")
    sandbox = sandbox_with_five_files

    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="read_file",
            description="Reads the content of a specific file.",
            parameters={
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
            handler=lambda filename: sandbox.read_text(filename),
        )
    )

    class FakeOllamaClientSingleFile:
        def __init__(self):
            self.step = 0

        def chat(self, messages, tools=None):
            self.step += 1
            if self.step == 1:
                print(" -> [Mock AI]: Requesting tool 'read_file' with filename='file_3.txt'...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        tool_calls=[
                            ToolCall(
                                function=FunctionCall(
                                    name="read_file",
                                    arguments={"filename": "file_3.txt"}
                                )
                            )
                        ]
                    ),
                    done=True
                )
            else:
                last_msg = messages[-1]
                print(f" -> [Mock AI]: Received from Tool: '{last_msg.content}'")
                print(" -> [Mock AI]: Formulating final answer in English...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        content=f"The code read from file_3.txt is 303 (content: {last_msg.content})"
                    ),
                    done=True
                )

    agent = AIAgent(client=FakeOllamaClientSingleFile(), tool_registry=registry)
    user_prompt = "Read file_3.txt and tell me the code inside."
    print(f" -> User Prompt: '{user_prompt}'")
    
    response = agent.run(user_prompt)
    print(f" -> Final AI Response: {response}")

    assert "303" in response
    assert "Report Gamma" in response


def test_agent_read_all_files_tool(sandbox_with_five_files: FileSandbox):
    """
    Tests requesting the AI to read and aggregate ALL files in the sandbox.
    """
    print("\n--- [UNIT TEST: AI Reads ALL Files in Folder] ---")
    sandbox = sandbox_with_five_files

    def read_all_files() -> str:
        files = sandbox.list_files()
        results = []
        for f in sorted(files):
            content = sandbox.read_text(f)
            results.append(f"[{f}]: {content}")
        return "\n".join(results)

    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="read_all_files",
            description="Reads all files in the sandbox directory.",
            parameters={"type": "object", "properties": {}},
            handler=read_all_files,
        )
    )

    class FakeOllamaClientAllFiles:
        def __init__(self):
            self.step = 0

        def chat(self, messages, tools=None):
            self.step += 1
            if self.step == 1:
                print(" -> [Mock AI]: Requesting tool 'read_all_files'...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        tool_calls=[
                            ToolCall(
                                function=FunctionCall(
                                    name="read_all_files",
                                    arguments={}
                                )
                            )
                        ]
                    ),
                    done=True
                )
            else:
                last_msg = messages[-1]
                print(f" -> [Mock AI]: Received tool output:\n{last_msg.content}")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        content=f"Successfully read all 5 files:\n{last_msg.content}"
                    ),
                    done=True
                )

    agent = AIAgent(client=FakeOllamaClientAllFiles(), tool_registry=registry)
    user_prompt = "Read all files in the directory and summarize them."
    print(f" -> User Prompt: '{user_prompt}'")

    response = agent.run(user_prompt)
    print(f" -> Final AI Response:\n{response}")

    assert "file_1.txt" in response
    assert "file_5.txt" in response
    assert "Code 101" in response
    assert "Code 505" in response
