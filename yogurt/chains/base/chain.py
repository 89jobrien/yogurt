from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseChain(ABC):
    """Base interface for all chains."""

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """The main execution method of the chain."""
        pass

class Chain(BaseChain):
    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """The main execution method of the chain."""
        pass