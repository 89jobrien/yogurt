from yogurt.callback_handlers.base import BaseCallbackHandler
from yogurt.output.base import LLMResult
from yogurt.output.streaming import StreamingChunk
from yogurt.pipes.base import BasePipe
from yogurt.prompts.prompt_value import PromptValue
from yogurt.utils.colorize import print_text # Assuming colorize is in utils


class StdOutCBH(BaseCallbackHandler):
    """A callback handler that prints to stdout for non-streaming events."""

    def on_pipe_start(self, pipe: BasePipe, inputs: dict) -> None:
        print_text(f"\n>>> Entering new pipe: {pipe.__class__.__name__}\n", "green")

    def on_llm_start(self, serialized: dict, inputs: dict) -> None:
        prompt_value = inputs.get('prompt')
        prompt_text = "N/A"
        if isinstance(prompt_value, PromptValue):
            prompt_text = prompt_value.text
        print_text(f"\n>>> Calling LLM\n", "cyan")
        print(prompt_text)

    def on_llm_end(self, response: LLMResult) -> None:
        print_text(f"\n\n>>> LLM Finished\n", "cyan")

    def on_pipe_end(self, outputs: dict) -> None:
        print_text(f"\n>>> Finished pipe\n", "green")

    def on_pipe_error(self, error: Exception) -> None:
        print_text(f"\n>>> Pipe Error: {error}", "red")

    def on_llm_error(self, error: Exception) -> None:
        print_text(f"\n>>> LLM Error: {error}", "red")

    def on_text(self, text: str) -> None:
        print_text(text, "green")


class StreamedStdOutCBH(BaseCallbackHandler):
    """A callback handler that streams LLM chunks to stdout."""

    def __init__(self):
        self.stream_color = "bright_blue"
        self.metadata_color = "yellow"

    # def on_llm_new_token(self, token: str) -> None:
    #     print_text(token, "cyan", end="", flush=True)

    def on_llm_stream(self, chunk: StreamingChunk) -> None:
        """
        Prints the text of the streaming chunk to the console in a
        consistent color.
        """
        if chunk.text:
            print_text(chunk.text, self.stream_color, end="")
    
        # if chunk.metadata:
        #     for key, value in chunk.metadata.items():
        #         print_text(f"\n{key}: {value}", self.metadata_color, end="")