from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseMemory(ABC):
    @abstractmethod
    def load_memory_variables(self) -> Dict[str, Any]:
        """Return key-value pairs of memory."""
        pass

    @abstractmethod
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save the context of this model run to memory."""
        pass
