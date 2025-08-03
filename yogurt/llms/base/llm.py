from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Iterator
from pydantic import Field, BaseModel, field_validator

from yogurt.messages.base import HumanMessage
from yogurt.output.streaming import StreamingChunk
from yogurt.output.base import LLMResult
from yogurt.prompts.prompt_value import PromptValue


class BaseLLM(BaseModel, ABC):
    """
    An abstract base class for LLMs that defines a pure interface.

    Every method is abstract, forcing subclasses to implement the full
    synchronous, asynchronous, and streaming contract. It also includes
    Pydantic-based configuration and validation.
    """

    temperature: float = Field(default=0.7, description="The sampling temperature.")
    model_name: str = "default-model"

    model_config = {
        "arbitrary_types_allowed": True,
    }

    @abstractmethod
    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Core logic for model generation. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def generate_prompt(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Generates a response from a structured PromptValue."""
        pass

    @abstractmethod
    def invoke(self, input_str: str, **kwargs: Any) -> str:
        """Generates a response from a simple string input."""
        pass

    @abstractmethod
    def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[StreamingChunk]:
        """Streams response chunks from a structured PromptValue."""
        pass

    @abstractmethod
    async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Asynchronously generates a response from a structured PromptValue."""
        pass

    @abstractmethod
    async def ainvoke(self, input_str: str, **kwargs: Any) -> str:
        """Asynchronously generates a response from a simple string input."""
        pass

    @abstractmethod
    async def astream(
        self, prompt: PromptValue, **kwargs: Any
    ) -> AsyncIterator[StreamingChunk]:
        """Asynchronously streams response chunks from a structured PromptValue."""
        pass

    @field_validator("temperature")
    @classmethod
    def check_temperature(cls, v: float) -> float:
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v


class LLM(BaseLLM):
    temperature: float = Field(default=0.7, description="The sampling temperature.")
    model_name: str = "default-model"

    @abstractmethod
    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        pass

    def generate_prompt(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """The main entry point for generating responses from a prompt."""
        return self._generate(prompt, **kwargs)

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        """A convenience method for simple string-in, string-out usage."""
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = self.generate_prompt(prompt, **kwargs)
        return result.generations[0].text

    @field_validator("temperature")
    @classmethod
    def check_temperature(cls, v: float) -> float:
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
