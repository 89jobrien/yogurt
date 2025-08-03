from typing import Any, List

from yogurt.chains.base import BaseChain
from yogurt.llms.base.llm import BaseLLM
from yogurt.prompts.prompt_template.prompt_template import BasePromptTemplate
from yogurt.callback_handlers.base import BaseCallbackHandler


class LLMChain(BaseChain):
    prompt: BasePromptTemplate
    llm: BaseLLM
    callbacks: List[BaseCallbackHandler] = []

    def __init__(
        self,
        prompt: BasePromptTemplate,
        llm: BaseLLM,
        callbacks: List[BaseCallbackHandler],
    ):
        self.prompt = prompt
        self.llm = llm
        self.callbacks = callbacks or []

    def run(self, **kwargs: Any) -> str:
        for handler in self.callbacks:
            handler.on_chain_start(self, inputs=kwargs)

        try:
            prompt_value = self.prompt.format_prompt(**kwargs)
            response = self.llm.generate_prompt(prompt_value)

            for handler in self.callbacks:
                handler.on_llm_end(response)

            return response.generations[0].text
        except Exception as e:
            for handler in self.callbacks:
                handler.on_chain_error(e)
            raise e
