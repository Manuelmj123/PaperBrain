import json
from pathlib import Path
from typing import Dict

from app.domain.interfaces.state_repository import StateRepository


class JsonStateRepository(StateRepository):
    def __init__(self, state_file: Path):
        self._state_file = state_file
        self._state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict:
        if not self._state_file.exists():
            return {}

        try:
            return json.loads(self._state_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save(self, state: Dict):
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )