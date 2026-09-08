from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AIConfig:
    """Configurações do motor de Inteligência Artificial local."""
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT", "60"))

    @property
    def generate_endpoint(self) -> str:
        return f"{self.base_url}/api/generate"

    @property
    def tags_endpoint(self) -> str:
        return f"{self.base_url}/api/tags"


default_config = AIConfig()
