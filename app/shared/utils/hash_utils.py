import hashlib
from pathlib import Path


def hash_file(path: Path) -> str:

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()