from abc import ABC
from yogurt.pipes.base import BasePipe
from yogurt.output.base import LLMResult
from yogurt.output.streaming import StreamingChunk


class BaseCallbackHandler(ABC):
    """Base interface for callback handlers."""

    def on_llm_stream(self, chunk: StreamingChunk) -> None:
        """Called when an LLM streams a new chunk."""
        pass

    # --- Existing methods ---
    def on_pipe_start(self, pipe: BasePipe, inputs: dict) -> None:
        """Called when a pipe starts."""
        pass

    def on_pipe_end(self, outputs: dict) -> None:
        """Called when a pipe ends."""
        pass

    def on_llm_start(self, serialized: dict, inputs: dict) -> None:
        """Called when an LLM starts."""
        pass

    def on_llm_new_token(self, token: str) -> None:
        """Called when an LLM generates a new token."""
        pass

    def on_llm_end(self, response: LLMResult) -> None:
        """Called when an LLM finishes."""
        pass

    def on_llm_error(self, error: Exception) -> None:
        """Called when an LLM encounters an error."""
        pass

    def on_pipe_error(self, error: Exception) -> None:
        """Called when a pipe encounters an error."""
        pass

    def on_text(self, text: str) -> None:
        """Called when text is generated."""
        pass