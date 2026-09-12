"""
Script de Demonstração: Leitura Segura de Ficheiros com Tool Calling (Ollama + AIAgent)
Cria 5 ficheiros com números e frases diferentes e pede à IA para consultar um deles.
"""

from pathlib import Path
from ai.config import AIConfig
from ai.client import OllamaClient
from ai.sandbox import FileSandbox
from ai.tools import ToolDefinition, ToolRegistry
from ai.agent import AIAgent


def setup_demo_files(sandbox: FileSandbox) -> None:
    """Cria 5 ficheiros distintos dentro da sandbox."""
    files_data = {
        "relatorio_financeiro.txt": "Saldo final apurado: 14500 euros",
        "codigo_acesso.txt": "PIN de seguranca: 9874",
        "temperatura_servidor.txt": "Temperatura atual: 42 graus Celsius",
        "contagem_utilizadores.txt": "Total de utilizadores ativos: 350",
        "versao_sistema.txt": "Numero da versao instalada: 204",
    }
    for filename, content in files_data.items():
        sandbox.write_text(filename, content)
    print(f"[OK] Criados {len(files_data)} ficheiros de teste na pasta sandbox: {sandbox.base_dir}")


def main():
    # 1. Configurar Sandbox isolada
    sandbox_path = Path(__file__).resolve().parent.parent / "tests" / "sandbox_data"
    sandbox = FileSandbox(base_dir=sandbox_path)
    setup_demo_files(sandbox)

    # 2. Configurar Registo de Ferramentas
    registry = ToolRegistry()

    # Ferramenta 1: Ler Ficheiro
    registry.register(
        ToolDefinition(
            name="ler_ficheiro",
            description="Lê o conteúdo de texto de um ficheiro dentro da pasta sandbox autorizada.",
            parameters={
                "type": "object",
                "properties": {
                    "nome_ficheiro": {
                        "type": "string",
                        "description": "O nome do ficheiro a ler (ex: codigo_acesso.txt, temperatura_servidor.txt)"
                    }
                },
                "required": ["nome_ficheiro"],
            },
            handler=lambda nome_ficheiro: sandbox.read_text(nome_ficheiro),
        )
    )

    # Ferramenta 2: Listar Ficheiros
    registry.register(
        ToolDefinition(
            name="listar_ficheiros",
            description="Lista os nomes de todos os ficheiros disponíveis na pasta autorizada.",
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=lambda: ", ".join(sandbox.list_files()),
        )
    )

    # 3. Inicializar Cliente e Agente
    client = OllamaClient(config=AIConfig())
    agent = AIAgent(
        client=client,
        tool_registry=registry,
        system_prompt="És um assistente útil e rigoroso. Quando te pedirem para consultar dados de ficheiros, deves usar a ferramenta 'ler_ficheiro' ou 'listar_ficheiros' para obter os dados reais."
    )

    prompt = "Lê o ficheiro 'codigo_acesso.txt' e diz-me qual é o PIN de segurança que está lá registado."
    print(f"\n[USER PROMPT]: {prompt}")
    print("[AGENTE]: A processar e a invocar ferramentas...\n")

    try:
        response = agent.run(prompt)
        print(f"[RESPOSTA FINAL DA IA]:\n{response}")
    except Exception as e:
        print(f"[ERRO OU OLLAMA OFFLINE]: {e}")
        print("\nPara executar com o Ollama real, certifica-te que o Ollama está ligado.")


if __name__ == "__main__":
    main()
