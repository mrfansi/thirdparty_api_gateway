from abc import ABC, abstractmethod
from typing import Any, Dict

class UseCase(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

class Repository(ABC):
    @abstractmethod
    def get(self, id: str) -> Dict:
        pass

    @abstractmethod
    def create(self, data: Dict) -> Dict:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict) -> Dict:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
