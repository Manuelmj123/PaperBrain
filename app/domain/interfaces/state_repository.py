from abc import ABC, abstractmethod
from typing import Dict


class StateRepository(ABC):

    @abstractmethod
    def load(self) -> Dict:
        pass

    @abstractmethod
    def save(self, state: Dict):
        pass