from pathlib import Path
import pytest

from ai.sandbox import FileSandbox, SandboxSecurityError
from ai.tools import ToolDefinition, ToolRegistry
from ai.agent import AIAgent
from ai.models import ChatMessage, ChatResponse, FunctionCall, ToolCall


@pytest.fixture
def sandbox_with_five_files(tmp_path: Path) -> FileSandbox:
    """Cria uma sandbox com 5 ficheiros distintos contendo frases e números."""
    sandbox = FileSandbox(base_dir=tmp_path / "sandbox")
    files = {
        "ficheiro_1.txt": "Relatório Alpha: Código 101",
        "ficheiro_2.txt": "Relatório Beta: Código 202",
        "ficheiro_3.txt": "Relatório Gamma: Código 303",
        "ficheiro_4.txt": "Relatório Delta: Código 404",
        "ficheiro_5.txt": "Relatório Epsilon: Código 505",
    }
    for filename, content in files.items():
        sandbox.write_text(filename, content)
    return sandbox


def test_sandbox_read_and_write(tmp_path: Path):
    print("\n--- [TESTE UNITÁRIO: Leitura e Escrita na Sandbox] ---")
    sandbox = FileSandbox(base_dir=tmp_path)
    sandbox.write_text("doc1.txt", "conteudo do teste 1")
    
    conteudo = sandbox.read_text("doc1.txt")
    ficheiros = sandbox.list_files()
    
    print(f" -> Conteúdo lido: '{conteudo}'")
    print(f" -> Ficheiros existentes: {ficheiros}")
    
    assert conteudo == "conteudo do teste 1"
    assert "doc1.txt" in ficheiros


def test_agent_read_single_file_tool(sandbox_with_five_files: FileSandbox):
    """
    Testa o pedido à IA para ler especificamente UM único ficheiro (ex: ficheiro_3.txt).
    """
    print("\n--- [TESTE UNITÁRIO: IA Lê UM Ficheiro Específico] ---")
    sandbox = sandbox_with_five_files

    # 1. Configurar Registo de Ferramentas
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="ler_ficheiro",
            description="Lê o conteúdo de um ficheiro específico.",
            parameters={
                "type": "object",
                "properties": {"nome": {"type": "string"}},
                "required": ["nome"],
            },
            handler=lambda nome: sandbox.read_text(nome),
        )
    )

    # 2. Mock do Cliente de IA simulando o pedido da Tool
    class FakeOllamaClientSingleFile:
        def __init__(self):
            self.step = 0

        def chat(self, messages, tools=None):
            self.step += 1
            if self.step == 1:
                print(" -> [IA Mock]: A invocar ferramenta 'ler_ficheiro' para 'ficheiro_3.txt'...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        tool_calls=[
                            ToolCall(
                                function=FunctionCall(
                                    name="ler_ficheiro",
                                    arguments={"nome": "ficheiro_3.txt"}
                                )
                            )
                        ]
                    ),
                    done=True
                )
            else:
                last_msg = messages[-1]
                print(f" -> [IA Mock]: Recebeu da Tool: '{last_msg.content}'")
                print(" -> [IA Mock]: A formular resposta final...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        content=f"O número lido no ficheiro_3.txt é: 303 (dados: {last_msg.content})"
                    ),
                    done=True
                )

    agent = AIAgent(client=FakeOllamaClientSingleFile(), tool_registry=registry)
    user_prompt = "Lê o ficheiro_3.txt e diz-me o código que lá está."
    print(f" -> Prompt do Utilizador: '{user_prompt}'")
    
    resposta = agent.run(user_prompt)
    print(f" -> Resposta Final da IA: {resposta}")

    assert "303" in resposta
    assert "Relatório Gamma" in resposta


def test_agent_read_all_files_tool(sandbox_with_five_files: FileSandbox):
    """
    Testa o pedido à IA para ler TODOS os ficheiros disponíveis na sandbox.
    """
    print("\n--- [TESTE UNITÁRIO: IA Lê TODOS os Ficheiros] ---")
    sandbox = sandbox_with_five_files

    def ler_todos_os_ficheiros() -> str:
        ficheiros = sandbox.list_files()
        resultados = []
        for f in sorted(ficheiros):
            conteudo = sandbox.read_text(f)
            resultados.append(f"[{f}]: {conteudo}")
        return "\n".join(resultados)

    # 1. Configurar Registo de Ferramentas
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="ler_todos_os_ficheiros",
            description="Lê todos os ficheiros existentes na pasta sandbox.",
            parameters={"type": "object", "properties": {}},
            handler=ler_todos_os_ficheiros,
        )
    )

    # 2. Mock do Cliente de IA simulando o pedido de leitura de todos os ficheiros
    class FakeOllamaClientAllFiles:
        def __init__(self):
            self.step = 0

        def chat(self, messages, tools=None):
            self.step += 1
            if self.step == 1:
                print(" -> [IA Mock]: A invocar ferramenta 'ler_todos_os_ficheiros'...")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        tool_calls=[
                            ToolCall(
                                function=FunctionCall(
                                    name="ler_todos_os_ficheiros",
                                    arguments={}
                                )
                            )
                        ]
                    ),
                    done=True
                )
            else:
                last_msg = messages[-1]
                print(f" -> [IA Mock]: Recebeu da Tool todos os dados:\n{last_msg.content}")
                return ChatResponse(
                    model="mock-model",
                    message=ChatMessage(
                        role="assistant",
                        content=f"Li todos os 5 ficheiros com sucesso:\n{last_msg.content}"
                    ),
                    done=True
                )

    agent = AIAgent(client=FakeOllamaClientAllFiles(), tool_registry=registry)
    user_prompt = "Quero que leias todos os ficheiros da pasta e me mostres o resumo."
    print(f" -> Prompt do Utilizador: '{user_prompt}'")

    resposta = agent.run(user_prompt)
    print(f" -> Resposta Final da IA:\n{resposta}")

    assert "ficheiro_1.txt" in resposta
    assert "ficheiro_5.txt" in resposta
    assert "Código 101" in resposta
    assert "Código 505" in resposta
