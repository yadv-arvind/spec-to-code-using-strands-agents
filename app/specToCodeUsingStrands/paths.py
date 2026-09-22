import tempfile
from pathlib import Path


def _resolve_sandbox() -> Path:
    """Prefer ./sandbox, fall back to a temp dir when the code dir is read-only.

    CodeZip runtimes mount the working directory (/var/task) read-only, so the
    agent's generated files have to land somewhere else once deployed.
    """
    local = Path(__file__).resolve().parent / "sandbox"
    try:
        local.mkdir(parents=True, exist_ok=True)
        probe = local / ".write-probe"
        probe.touch()
        probe.unlink()
        return local
    except OSError:
        fallback = Path(tempfile.gettempdir()) / "sandbox"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


SANDBOX_DIR = _resolve_sandbox()
