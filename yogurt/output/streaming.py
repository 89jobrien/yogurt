from typing import Dict, Any
from pydantic import BaseModel, Field


class StreamingChunk(BaseModel):
    """
    Represents a single chunk of a streaming response from an LLM.

    This model captures the text part of the chunk and any associated
    metadata sent by the provider for that specific piece of the stream.
    """

    text: str
    """The text content of this specific chunk."""
    chunk_info: Dict[str, Any] = Field(default_factory=dict)
    """Any additional metadata provided by the LLM for this chunk."""
