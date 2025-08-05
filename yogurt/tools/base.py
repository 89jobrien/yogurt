from abc import abstractmethod
from typing import Protocol, Any, Dict


class BaseTool(Protocol):
    name: str
    description: str

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Returns the tool's schema in Ollama/OpenAI format."""
        pass
