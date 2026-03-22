from abc import ABC, abstractmethod


class LlmClient(ABC):

    @abstractmethod
    def ask(self, question: str, context: str):
        pass