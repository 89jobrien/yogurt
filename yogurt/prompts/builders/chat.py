from typing import List, Any
from yogurt.prompts.builders.base import BasePromptBuilder
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import BaseMessage, SystemMessage, HumanMessage

class ChatPromptBuilder(BasePromptBuilder):
    """A prompt template for creating conversational message lists."""
    
    def __init__(self, system_msg: str, human_msg: str):
        self.system_template = system_msg
        self.human_template = human_msg

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Formats the templates into a list of messages."""
        system_message = SystemMessage(content=self.system_template.format(**kwargs))
        human_message = HumanMessage(content=self.human_template.format(**kwargs))
        
        # Returns a PromptValue containing the list of messages
        return PromptValue(messages=[system_message, human_message])