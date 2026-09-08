from typing import Optional
import requests

from .config import AIConfig, default_config
from .models import PromptRequest, PromptResponse


class AIClientError(Exception):
    """Exceção base para erros na comunicação com a IA."""
    pass


class AIServiceUnavailableError(AIClientError):
    """O serviço de IA local não está acessível ou está desligado."""
    pass


class OllamaClient:
    """Cliente dedicado para comunicação com a API REST do Ollama local."""

    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or default_config

    def generate(self, prompt: str, system: Optional[str] = None, model: Optional[str] = None) -> PromptResponse:
        """
        Envia um prompt para inferência no modelo local e devolve a resposta estruturada.
        """
        selected_model = model or self.config.model
        request_data = PromptRequest(
            prompt=prompt,
            model=selected_model,
            system=system,
            stream=False,
        )

        payload = {
            "model": request_data.model,
            "prompt": request_data.prompt,
            "stream": request_data.stream,
        }
        if request_data.system:
            payload["system"] = request_data.system

        try:
            response = requests.post(
                self.config.generate_endpoint,
                json=payload,
                timeout=self.config.timeout_seconds,
            )
        except requests.exceptions.ConnectionError as exc:
            raise AIServiceUnavailableError(
                f"Falha ao conectar com o Ollama em {self.config.base_url}. "
                "Executa o script de inicialização em 'setup/' primeiro."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise AIClientError(
                f"Tempo limite excedido ({self.config.timeout_seconds}s) na geração do modelo '{selected_model}'."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise AIClientError(f"Erro na requisição à API: {exc}") from exc

        if response.status_code != 200:
            raise AIClientError(
                f"Ollama retornou erro {response.status_code}: {response.text}"
            )

        data = response.json()
        duration_ns = data.get("total_duration")
        duration_ms = (duration_ns / 1_000_000) if duration_ns else None

        return PromptResponse(
            model=data.get("model", selected_model),
            response=data.get("response", ""),
            done=data.get("done", True),
            total_duration_ms=duration_ms,
            prompt_eval_count=data.get("prompt_eval_count"),
            eval_count=data.get("eval_count"),
        )
