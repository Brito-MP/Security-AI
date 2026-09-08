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
    Verifica se o servidor Ollama está online e lista os modelos disponíveis
    sem consumir tokens nem invocar inferência.
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
            error_message=f"Servidor retornou código {response.status_code}",
        )
    except requests.exceptions.ConnectionError:
        return HealthStatus(
            is_online=False,
            error_message=f"Não foi possível ligar a {cfg.base_url}. O Ollama está em execução?",
        )
    except Exception as exc:
        return HealthStatus(
            is_online=False,
            error_message=str(exc),
        )


def is_model_available(model_name: str, config: Optional[AIConfig] = None) -> bool:
    """Verifica se um modelo específico está carregado no servidor local."""
    status = check_ai_service(config)
    if not status.is_online:
        return False
    
    # Modelos no Ollama podem ter tags como ":latest" ou versão explícita
    target = model_name.lower()
    return any(target in m.lower() for m in status.available_models)


if __name__ == "__main__":
    status = check_ai_service()
    print("=" * 45)
    print("        ESTADO DA IA LOCAL (OLLAMA)")
    print("=" * 45)
    if status.is_online:
        print(f" [ESTADO]  ONLINE (HTTP {status.status_code})")
        print(f" [URL]     {default_config.base_url}")
        print(" [MODELOS DISPONÍVEIS]:")
        for m in status.available_models:
            print(f"   • {m}")
    else:
        print(" [ESTADO]  OFFLINE")
        print(f" [MOTIVO]  {status.error_message}")
    print("=" * 45)

