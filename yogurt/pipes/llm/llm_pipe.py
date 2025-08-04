from typing import Any, List, Optional, Iterator, AsyncIterator, Dict

from yogurt.pipes import BasePipe
from yogurt.llms import BaseLLM
from yogurt.prompts.builders import BasePromptBuilder
from yogurt.callback_handlers.base import BaseCallbackHandler
from yogurt.parsers.output_parsers import OutputParser
from yogurt.output.streaming import StreamingChunk



class LLMPipe(BasePipe):
    """
    A pipe that handles the full flow from prompt to structured output:
    1. Formats a prompt with user input.
    2. Calls an LLM to get a response.
    3. If an output_parser is provided, it parses the raw text into a
       structured format. Otherwise, it returns the raw text.
    """
    prompt: BasePromptBuilder
    llm: BaseLLM
    output_parser: Optional[OutputParser] = None
    callbacks: List[BaseCallbackHandler] = []
    output_key: str = "text"

    def __init__(
        self,
        prompt: BasePromptBuilder,
        llm: BaseLLM,
        callbacks: List[BaseCallbackHandler],
        output_parser: Optional[OutputParser] = None,
        output_key: str = "text",
    ):
        self.prompt = prompt
        self.llm = llm
        self.callbacks = callbacks or []
        self.output_parser = output_parser
        self.output_key = output_key


    @property
    def input_keys(self) -> List[str]:
        """Input keys are determined by the prompt's input variables."""
        # Assuming the prompt builder has an 'input_variables' attribute.
        # This would need to be added to your BasePromptBuilder.
        return getattr(self.prompt, 'input_variables', [])
    
    @property
    def output_keys(self) -> List[str]:
        """The single output key for this pipe."""
        return [self.output_key]
    

    def run(self, **kwargs: Any) -> Dict[str, Any]:
        for handler in self.callbacks:
            handler.on_chain_start(self, inputs=kwargs)
        try:
            prompt_value = self.prompt.format_prompt(**kwargs)
            for handler in self.callbacks:
                handler.on_llm_start(serialized={}, inputs={"prompt": prompt_value})
            response = self.llm.generate(prompt_value)
            raw_text = response.generations[0].text

            for handler in self.callbacks:
                handler.on_llm_end(response)

            output = self.output_parser.parse(raw_text) if self.output_parser else raw_text
            return {self.output_key: output}
        
        except Exception as e:
            for handler in self.callbacks:
                handler.on_chain_error(e)
            raise e

    async def arun(self, **kwargs: Any) -> Any:
        """
        Asynchronously runs the pipe and returns either raw text or parsed output.
        """
        for handler in self.callbacks:
            handler.on_chain_start(self, inputs=kwargs)

        try:
            prompt_value = self.prompt.format_prompt(**kwargs)
            response = await self.llm.agenerate(prompt_value)
            raw_text = response.generations[0].text

            for handler in self.callbacks:
                handler.on_llm_end(response)

            output = self.output_parser.parse(raw_text) if self.output_parser else raw_text
            return {self.output_key: output}

        except Exception as e:
            for handler in self.callbacks:
                handler.on_chain_error(e)
            raise e
        
    def predict(self, **kwargs: Any) -> Any:
        return self.run(**kwargs)[self.output_key]
    
    async def apredict(self, **kwargs: Any) -> Any:
        result = await self.arun(**kwargs)
        return result[self.output_key]

    def stream(self, **kwargs: Any) -> Iterator[StreamingChunk]:
        for handler in self.callbacks:
            handler.on_chain_start(self, inputs=kwargs)
        try:
            prompt_value = self.prompt.format_prompt(**kwargs)
            for handler in self.callbacks:
                handler.on_llm_start(serialized={}, inputs={"prompt": prompt_value})


            for chunk in self.llm.stream(prompt_value):
                for handler in self.callbacks:
                    handler.on_llm_stream(chunk)
                yield chunk

        except Exception as e:
            for handler in self.callbacks:
                handler.on_chain_error(e)
            raise e
        
    
    async def astream(self, **kwargs: Any) -> AsyncIterator[StreamingChunk]:
        for handler in self.callbacks:
            handler.on_chain_start(self, inputs=kwargs)

        try:
            prompt_value = self.prompt.format_prompt(**kwargs)
            for handler in self.callbacks:
                handler.on_llm_start(serialized={}, inputs={"prompt": prompt_value})

            async for chunk in self.llm.astream(prompt_value):
                for handler in self.callbacks:
                    handler.on_llm_stream(chunk)
                yield chunk

        except Exception as e:
            for handler in self.callbacks:
                handler.on_chain_error(e)
            raise e