from abc import ABC, abstractmethod
from typing import Any
from yogurt.prompts.prompt_value import PromptValue


class BasePromptTemplate(ABC):
    """Base interface for all prompt templates."""

    @abstractmethod
    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Create a PromptValue from user input."""
        pass


class PromptTemplate(BasePromptTemplate):
    """A simple prompt template that takes a single input and returns a PromptValue."""

    def __init__(self, template: str):
        self.template = template

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        return PromptValue(text=self.template.format(**kwargs))
