import re
from abc import abstractmethod
from typing import Protocol, Any, List
from yogurt.output.streaming import StreamingChunk
from yogurt.messages.base import BaseMessage, HumanMessage, AIMessage, SystemMessage



class BaseOutputParser(Protocol):
    @abstractmethod
    def parse(self, text: str) -> Any:
        pass

    @abstractmethod
    def parse_chunk(self, text: StreamingChunk) -> Any:
        pass

    @abstractmethod
    def get_format_instructions(self) -> str:
        pass


class OutputParser:
    def parse(self, text: str) -> List[BaseMessage]:
        """
        Parses text into a list of BaseMessage objects.
        Expects messages like: '[role] content'
        """
        pattern = re.compile(r"^\[(human|ai|system)\]\s*(.+)$", re.MULTILINE | re.IGNORECASE)
        messages: List[BaseMessage] = []

        role_to_cls = {
            "human": HumanMessage,
            "ai": AIMessage,
            "system": SystemMessage,
        }

        for match in pattern.finditer(text):
            role = match.group(1).lower()
            content = match.group(2).strip()
            cls = role_to_cls.get(role, BaseMessage)
            if cls:
                messages.append(cls(content=content))

        return messages
    
    def parse_chunk(self, text: StreamingChunk) -> List[BaseMessage]:
        return self.parse(text.text)

    def get_format_instructions(self) -> str:
        return (
            "Format messages with role names in brackets, e.g.:\n"
            "[system] You are a helpful assistant.\n"
            "[human] Hello!\n"
            "[ai] Hi, how can I help you?\n"
            "The parser will extract each message into its structured representation."
        )