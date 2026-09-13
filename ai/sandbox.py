from pathlib import Path
from typing import List, Union


class SandboxSecurityError(Exception):
    """Raised when an unauthorized path access attempt occurs outside the sandbox directory."""
    pass


class FileSandbox:
    """
    Filesystem sandbox providing strict encapsulation.
    Guarantees that all file read/write operations remain confined inside the base directory,
    preventing Path Traversal vulnerabilities (e.g., ../../etc/shadow).
    """

    def __init__(self, base_dir: Union[str, Path]):
        self._base_dir = Path(base_dir).resolve()
        if not self._base_dir.exists():
            self._base_dir.mkdir(parents=True, exist_ok=True)

    @property
    def base_dir(self) -> Path:
        """Returns the resolved sandbox root directory (read-only)."""
        return self._base_dir

    def _resolve_safe_path(self, relative_path: str) -> Path:
        """
        Resolves the file path and strictly validates boundary containment.
        """
        target_path = (self._base_dir / relative_path).resolve()

        try:
            target_path.relative_to(self._base_dir)
        except ValueError as exc:
            raise SandboxSecurityError(
                f"Access denied: path '{relative_path}' attempts to traverse outside the allowed sandbox folder."
            ) from exc

        return target_path

    def read_text(self, relative_path: str, encoding: str = "utf-8") -> str:
        """
        Safely reads text content from a file within the sandbox.
        """
        safe_path = self._resolve_safe_path(relative_path)

        if not safe_path.exists() or not safe_path.is_file():
            raise FileNotFoundError(f"File '{relative_path}' not found in sandbox.")

        return safe_path.read_text(encoding=encoding)

    def write_text(self, relative_path: str, content: str, encoding: str = "utf-8") -> None:
        """
        Safely writes text content to a file within the sandbox.
        """
        safe_path = self._resolve_safe_path(relative_path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding=encoding)

    def list_files(self) -> List[str]:
        """
        Lists all regular files located at the root of the sandbox directory.
        """
        if not self._base_dir.exists():
            return []
        return [f.name for f in self._base_dir.iterdir() if f.is_file()]
