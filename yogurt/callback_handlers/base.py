from abc import ABC
from yogurt.pipes.base import BasePipe
from yogurt.output.base import LLMResult


class BaseCallbackHandler(ABC):
    """Base interface for callback handlers."""

    def on_chain_start(self, chain: BasePipe, inputs: dict) -> None:
        """Called when a chain starts."""
        pass

    def on_llm_end(self, response: LLMResult) -> None:
        """Called when an LLM finishes."""
        pass

    def on_chain_error(self, error: Exception) -> None:
        """Called when a chain encounters an error."""
        pass
