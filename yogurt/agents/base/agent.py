from pydantic import BaseModel

class AgentAction(BaseModel):
    tool: str
    tool_input: str

class AgentFinish(BaseModel):
    output: str