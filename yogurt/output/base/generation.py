from typing import List, Dict, Any
from pydantic import BaseModel, Field

class Generation(BaseModel):
    """The output of one LLM generation."""
    text: str
    """The generated text."""
    generation_info: Dict[str, Any] = Field(default_factory=dict)
    """Additional generation data, e.g., token usage, finish reason."""
