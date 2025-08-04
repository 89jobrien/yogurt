from typing import Literal, TypeAlias
from pydantic import BaseModel


class BaseMessage(BaseModel):
    """The base class for a message."""

    content: str
    role: str

    def __str__(self):
        return self.content


class HumanMessage(BaseMessage):
    """A message from a human."""

    role: Literal["human"] = "human"


class AIMessage(BaseMessage):
    """A message from the AI."""

    role: Literal["ai"] = "ai"


class SystemMessage(BaseMessage):
    """A system message that sets the context for the AI."""

    role: Literal["system"] = "system"


AnyMessage: TypeAlias = HumanMessage | AIMessage | SystemMessage | BaseMessage