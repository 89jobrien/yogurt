from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class AgentAction(BaseModel):
    input: str
    tool_choice: Optional[ToolCall] = None
    output: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentFinish(BaseModel):
    output: str
