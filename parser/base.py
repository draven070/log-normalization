from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def can_parse(self, log: str) -> bool:
        pass

    @abstractmethod
    def parse(self, log: str):
        pass