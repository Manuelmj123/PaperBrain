from pathlib import Path
from typing import List

from app.core.constants import SUPPORTED_EXTENSIONS


def is_supported_file(path: Path) -> bool:

    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def list_supported_files(root: Path) -> List[Path]:

    return [
        p
        for p in root.rglob("*")
        if p.is_file() and is_supported_file(p)
    ]


def relative_source(root: Path, file_path: Path) -> str:

    return str(file_path.relative_to(root))