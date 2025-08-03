from abc import ABC, abstractmethod
from typing import List, Any
from yogurt.messages import AIMessage, HumanMessage
from yogurt.prompts.base import PromptValue
from yogurt.output.base import LLMResult

class BaseLLM(ABC):
    """Base interface for all language models."""

    @abstractmethod
    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """
        The core logic for model generation. This should not be called directly.
        It takes a formatted PromptValue and returns an LLMResult.
        """
        pass

    def generate_prompt(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """The main entry point for generating responses from a prompt."""
        raise NotImplementedError

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        """A convenience method for simple string-in, string-out usage."""
        raise NotImplementedError
    
class LLM(BaseLLM):
    @abstractmethod
    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """
        The core logic for model generation. This should not be called directly.
        It takes a formatted PromptValue and returns an LLMResult.
        """
        pass

    def generate_prompt(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """The main entry point for generating responses from a prompt."""
        return self._generate(prompt, **kwargs)

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        """A convenience method for simple string-in, string-out usage."""
        # This is a default implementation that can be optimized by subclasses.
        # It creates a temporary prompt value for the simple string input.
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = self.generate_prompt(prompt, **kwargs)
        return result.generations[0].text