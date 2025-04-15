import tempfile
from pathlib import Path


def getfile(content: str, extension: str, delete: bool = False) -> Path:
    with tempfile.NamedTemporaryFile(delete=delete, suffix=extension, mode="w") as f:
        f.write(content)
    return Path(f.name)
