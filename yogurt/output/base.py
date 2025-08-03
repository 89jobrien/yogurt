from typing import Dict, Any, List
from pydantic import BaseModel, Field


class Generation(BaseModel):
    """
    Represents a single, complete unit of generated text from an LLM.
    This is typically the final output after a non-streaming call.
    """

    text: str
    """The generated text content."""
    generation_info: Dict[str, Any] = Field(default_factory=dict)
    """Any additional metadata from the LLM provider for this generation."""


class LLMResult(BaseModel):
    """The complete result of an LLM call."""

    generations: List[Generation]
    """A list of generated responses."""
    llm_output: Dict[str, Any] = Field(default_factory=dict)
    """Any additional output from the LLM provider."""