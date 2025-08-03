import re
from yogurt.parsers.output_parsers.base import BaseOutputParser
from yogurt.agents.base import AgentAction, AgentFinish

class ReActOutputParser(BaseOutputParser):
    def parse(self, text: str) -> AgentAction | AgentFinish:
        # This regex looks for a pattern like: Action: [Tool Name], Action Input: [Input]
        action_match = re.search(r"Action: (.*?), Action Input: (.*)", text)
        
        if action_match:
            tool = action_match.group(1).strip()
            tool_input = action_match.group(2).strip()
            return AgentAction(tool=tool, tool_input=tool_input)
        
        return AgentFinish(output=text)