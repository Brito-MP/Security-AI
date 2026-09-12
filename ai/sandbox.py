from pathlib import Path
from typing import List


class SandboxSecurityError(Exception):
    """Exceção levantada quando há tentativa de acesso fora do diretório da sandbox."""
    pass


class FileSandbox:
    """
    Sandbox de sistema de ficheiros com encapsulamento estrito.
    Garante que qualquer leitura fica contida no diretório base especificado,
    prevenindo ataques de Path Traversal (ex: ../../etc/passwd).
    """

    def __init__(self, base_dir: str | Path):
        self._base_dir = Path(base_dir).resolve()
        if not self._base_dir.exists():
            self._base_dir.mkdir(parents=True, exist_ok=True)

    @property
    def base_dir(self) -> Path:
        """Devolve o caminho resolvido da sandbox (apenas leitura)."""
        return self._base_dir

    def _resolve_safe_path(self, relative_path: str) -> Path:
        """
        Resolve o caminho e valida estritamente se permanece dentro da sandbox.
        """
        # Resolve removendo referências relativas como ../
        target_path = (self._base_dir / relative_path).resolve()

        # Validação estrita de contenção
        try:
            target_path.relative_to(self._base_dir)
        except ValueError as exc:
            raise SandboxSecurityError(
                f"Acesso negado: o caminho '{relative_path}' tenta aceder fora da pasta sandbox permitida."
            ) from exc

        return target_path

    def read_text(self, relative_path: str, encoding: str = "utf-8") -> str:
        """
        Lê com segurança o conteúdo de texto de um ficheiro dentro da sandbox.
        """
        safe_path = self._resolve_safe_path(relative_path)

        if not safe_path.exists() or not safe_path.is_file():
            raise FileNotFoundError(f"Ficheiro '{relative_path}' não encontrado na sandbox.")

        return safe_path.read_text(encoding=encoding)

    def write_text(self, relative_path: str, content: str, encoding: str = "utf-8") -> None:
        """
        Escreve um ficheiro dentro da sandbox de forma segura.
        """
        safe_path = self._resolve_safe_path(relative_path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding=encoding)

    def list_files(self) -> List[str]:
        """
        Lista todos os ficheiros contidos na raiz da sandbox.
        """
        if not self._base_dir.exists():
            return []
        return [f.name for f in self._base_dir.iterdir() if f.is_file()]
