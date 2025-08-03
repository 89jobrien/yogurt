from typing import List, Dict, Any
from pydantic import BaseModel, Field

from yogurt.output.base import Generation


class LLMResult(BaseModel):
    """The complete result of an LLM call."""

    generations: List[Generation]
    """A list of generated responses."""
    llm_output: Dict[str, Any] = Field(default_factory=dict)
    """Any additional output from the LLM provider."""
