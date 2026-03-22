from abc import ABC, abstractmethod
from pathlib import Path


class FileReader(ABC):

    @abstractmethod
    def read(self, path: Path):
        pass