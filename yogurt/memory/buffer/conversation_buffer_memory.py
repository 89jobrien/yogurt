from typing import Dict, Any, List
from yogurt.memory.base import BaseMemory
from yogurt.messages.base import BaseMessage, HumanMessage, AIMessage


class ConversationBufferMemory(BaseMemory):
    memory_key: str = "history"
    chat_history: List[BaseMessage] = []

    def load_memory_variables(self) -> Dict[str, Any]:
        return {self.memory_key: self.chat_history}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        # Assuming one input key and one output key for simplicity
        input_str = next(iter(inputs.values()))
        output_str = next(iter(outputs.values()))
        self.chat_history.append(HumanMessage(content=input_str))
        self.chat_history.append(AIMessage(content=output_str))
