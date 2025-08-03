from abc import ABC, abstractmethod
from typing import Any


class BaseChain(ABC):
    """Base interface for all chains."""

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """The main execution method of the chain."""
        raise NotImplementedError

    @abstractmethod
    async def arun(self, **kwargs: Any) -> Any:
        raise NotImplementedError
