import inspect
from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass(frozen=True)
class ToolDefinition:
    """
    Definição imutável de uma ferramenta exposta à IA.
    Contém os metadados JSON Schema e o callback de execução.
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable[..., Any]


class ToolRegistry:
    """
    Registo central de ferramentas/funções com total encapsulamento e tolerância a falhas.
    Mapeia os esquemas para a API do Ollama e executa handlers isoladamente,
    filtrando argumentos espúrios gerados por modelos mais pequenos.
    """

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Regista uma nova ferramenta no catálogo."""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> ToolDefinition:
        """Devolve a definição da ferramenta pelo nome."""
        if name not in self._tools:
            raise KeyError(f"Ferramenta '{name}' não está registada.")
        return self._tools[name]

    def get_schemas(self) -> List[Dict[str, Any]]:
        """
        Retorna a lista de especificações compatíveis com o padrão OpenAI/Ollama Tools.
        """
        schemas = []
        for tool in self._tools.values():
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
            })
        return schemas

    def execute(self, name: str, arguments: Dict[str, Any]) -> str:
        """
        Executa o handler associado à ferramenta de forma segura e converte o retorno para string.
        Filtra automaticamente argumentos que a função não aceita para evitar 'unexpected keyword argument'.
        """
        if name not in self._tools:
            return f"Erro: Ferramenta desconhecida '{name}'."

        tool = self._tools[name]
        try:
            # Inspeção dinâmica da assinatura do handler para filtrar apenas argumentos válidos
            sig = inspect.signature(tool.handler)
            has_var_keyword = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )

            if has_var_keyword:
                clean_args = arguments
            else:
                valid_param_names = set(sig.parameters.keys())
                clean_args = {k: v for k, v in arguments.items() if k in valid_param_names}

            result = tool.handler(**clean_args)
            return str(result)
        except Exception as exc:
            return f"Erro ao executar '{name}': {exc}"
