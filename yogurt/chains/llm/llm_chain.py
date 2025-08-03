from yogurt.chains.base import BaseChain
from typing import Any
from yogurt.chains.base.chain import BaseChain
from yogurt.llms.base.llm import BaseLLM
from yogurt.prompts.base.prompt_template import BasePromptTemplate

class LLMChain(BaseChain):
    """A chain that combines a prompt template with a language model."""
    prompt: BasePromptTemplate
    llm: BaseLLM

    def __init__(self, prompt: BasePromptTemplate, llm: BaseLLM):
        self.prompt = prompt
        self.llm = llm

    def run(self, **kwargs: Any) -> str:
        """
        Formats the prompt, passes it to the LLM, and returns the
        generated text.
        """
        prompt_value = self.prompt.format_prompt(**kwargs)
        
        # CORRECT: Use generate_prompt for PromptValue objects
        response = self.llm.generate_prompt(prompt_value)
        
        return response.generations[0].text