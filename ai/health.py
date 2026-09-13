import requests
from typing import Optional

try:
    from .config import AIConfig, default_config
    from .models import HealthStatus
except ImportError:
    from ai.config import AIConfig, default_config
    from ai.models import HealthStatus


def check_ai_service(config: Optional[AIConfig] = None) -> HealthStatus:
    """
    Checks if the local Ollama server is online and queries available models
    without triggering model inference or consuming tokens.
    """
    cfg = config or default_config

    try:
        response = requests.get(cfg.tags_endpoint, timeout=3)
        if response.status_code == 200:
            data = response.json()
            models = [item.get("name", "") for item in data.get("models", [])]
            return HealthStatus(
                is_online=True,
                status_code=response.status_code,
                available_models=models,
            )
        return HealthStatus(
            is_online=False,
            status_code=response.status_code,
            error_message=f"Server returned status code {response.status_code}",
        )
    except requests.exceptions.ConnectionError:
        return HealthStatus(
            is_online=False,
            error_message=f"Failed to connect to {cfg.base_url}. Is the Ollama service running?",
        )
    except Exception as exc:
        return HealthStatus(
            is_online=False,
            error_message=str(exc),
        )


def is_model_available(model_name: str, config: Optional[AIConfig] = None) -> bool:
    """Checks whether a specific model tag is available in the local Ollama registry."""
    status = check_ai_service(config)
    if not status.is_online:
        return False
    
    target = model_name.lower()
    return any(target in m.lower() for m in status.available_models)


if __name__ == "__main__":
    status = check_ai_service()
    print("=" * 45)
    print("        LOCAL AI STATUS (OLLAMA)")
    print("=" * 45)
    if status.is_online:
        print(f" [STATUS]  ONLINE (HTTP {status.status_code})")
        print(f" [URL]     {default_config.base_url}")
        print(" [AVAILABLE MODELS]:")
        for m in status.available_models:
            print(f"   • {m}")
    else:
        print(" [STATUS]  OFFLINE")
        print(f" [REASON]  {status.error_message}")
    print("=" * 45)
