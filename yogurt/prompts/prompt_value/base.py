from typing import List
from pydantic import BaseModel, Field
from yogurt.messages.base import BaseMessage


class PromptValue(BaseModel):
    """A container for a formatted prompt, ready for an LLM."""

    text: str = ""
    messages: List[BaseMessage] = Field(default_factory=list)

    def to_string(self) -> str:
        """Return the prompt as a single string."""
        if self.text:
            return self.text
        return "\\n".join([str(msg) for msg in self.messages])

    def to_messages(self) -> List[BaseMessage]:
        """Return the prompt as a list of messages."""
        return self.messages
