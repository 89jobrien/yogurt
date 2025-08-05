import re
from typing import List, Any
from yogurt.prompts.builders.base import BasePromptBuilder
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import BaseMessage, SystemMessage, HumanMessage

class ChatPromptBuilder(BasePromptBuilder):
    """A prompt template for creating conversational message lists."""
    system_template: str
    human_template: str
    input_variables: List[str]

    def __init__(self, system_msg: str, human_msg: str):
        self.system_template = system_msg
        self.human_template = human_msg
        self.input_variables = self._get_variables(system_msg + human_msg)

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the object."""
        return (
            f"{self.__class__.__name__}(\n"
            f"input_variables={self.input_variables},\n"
            f"system_template='{self.system_template}',\n"
            f"human_template='{self.human_template}'\n"
            f")"
        )

    def _get_variables(self, template: str) -> List[str]:
        """Uses regex to find all unique variables in a f-string template."""
        return sorted(list(set(re.findall(r"\{(\w+)\}", template))))

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Formats the templates into a list of messages."""
        system_message = SystemMessage(content=self.system_template.format(**kwargs))
        human_message = HumanMessage(content=self.human_template.format(**kwargs))
        
        # Returns a PromptValue containing the list of messages
        return PromptValue(messages=[system_message, human_message])