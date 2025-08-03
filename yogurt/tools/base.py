from abc import abstractmethod
from typing import Protocol, Any


class BaseTool(Protocol):
    name: str
    description: str

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        pass
