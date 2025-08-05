import json
import re
from typing import List, Any

from yogurt.constants.json_format import JSON_RESPONSE
from yogurt.output.streaming import StreamingChunk
from yogurt.parsers.output_parsers.base import BaseOutputParser
from yogurt.messages.base import SystemMessage, HumanMessage, AIMessage, BaseMessage
from yogurt.utils.json_parsing import parse_json_markdown, parse_partial_json


class JsonResponseParser(BaseOutputParser):
    """
    Parses a JSON string from an LLM into a list of Message objects.
    """

    def __init__(self):
        self.buffer = ""
        self.parsed_message_count = 0

    def parse_response(self, text: str) -> List[BaseMessage]:
        """
        Extracts a JSON object from a string and parses it into messages.
        It can handle JSON enclosed in markdown-style code fences.
        """
        parsed_json = parse_json_markdown(text)

        if parsed_json is None or "conversation" not in parsed_json:
            return []

        return self._parse_json_to_messages(parsed_json)

    def parse_streaming_chunk(self, chunk: StreamingChunk) -> Any:
        """
        Accumulates text from a chunk and parses the buffer to find
        any new, complete messages.
        """
        self.buffer += chunk.text

        parsed_json = parse_partial_json(self.buffer)

        # Attempt to parse the current buffer as partial JSON
        parsed_json = parse_partial_json(self.buffer)

        if parsed_json is None or "conversation" not in parsed_json:
            return []

        all_messages = self._parse_json_to_messages(parsed_json)

        # Check if we have found more complete messages than we've already yielded
        if len(all_messages) > self.parsed_message_count:
            new_messages = all_messages[self.parsed_message_count :]
            self.parsed_message_count = len(all_messages)
            return new_messages

        return []

    def parse(self, text: str) -> List[BaseMessage]:
        return self.parse_response(text)

    def parse_chunk(self, text: StreamingChunk) -> Any:
        return self.parse_streaming_chunk(text)

    def _parse_json_to_messages(self, parsed_json: dict) -> List[BaseMessage]:
        """Helper function to convert a parsed JSON dict to message objects."""
        messages: List[BaseMessage] = []
        role_to_cls = {
            "system": SystemMessage,
            "human": HumanMessage,
            "ai": AIMessage,
        }

        for msg_data in parsed_json.get("conversation", []):
            role = msg_data.get("role")
            content = msg_data.get("content")
            cls = role_to_cls.get(role)

            if cls and content is not None:
                messages.append(cls(content=content))

        return messages

    def get_response_format(self) -> str:
        """
        Returns clear instructions for the LLM on how to format its output.
        """
        return JSON_RESPONSE
