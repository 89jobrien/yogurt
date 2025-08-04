from abc import ABC, abstractmethod
from typing import Any
from yogurt.prompts.prompt_value import PromptValue


class BasePromptBuilder(ABC):
    """Base interface for all prompt builders."""

    @abstractmethod
    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Create a PromptValue from user input."""
        pass


class PromptBuilder(BasePromptBuilder):
    """A simple prompt builder that takes a single input and returns a PromptValue."""

    def __init__(self, template: str):
        self.template = template

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        return PromptValue(text=self.template.format(**kwargs))
