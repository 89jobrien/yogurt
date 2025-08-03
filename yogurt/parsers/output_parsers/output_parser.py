from abc import abstractmethod
from typing import Protocol, Any


class BaseOutputParser(Protocol):
    @abstractmethod
    def parse(self, text: str) -> Any:
        pass

    @abstractmethod
    def get_format_instructions(self) -> str:
        pass


class OutputParser:
    def parse(self, text: str) -> Any:
        """
        Example implementation: simply returns the text uppercased.
        Override this with real parsing logic as needed.
        """
        return text.upper()

    def get_format_instructions(self) -> str:
        """
        Example implementation: instructs that input will be uppercased.
        Override this with real instructions as needed.
        """
        return "Provide a string. The parser will return the string in uppercase."
