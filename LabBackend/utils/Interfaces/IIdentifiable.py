from abc import ABC, abstractmethod

class IIdentifiable(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        pass