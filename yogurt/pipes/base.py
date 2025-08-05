from abc import ABC, abstractmethod
from typing import Any


class BasePipe(ABC):
    """Base interface for all pipes."""

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """The main execution method of the pipe."""
        raise NotImplementedError

    @abstractmethod
    async def arun(self, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def stream(self, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def astream(self, **kwargs: Any) -> Any:
        raise NotImplementedError
