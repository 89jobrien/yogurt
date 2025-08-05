from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel, Field
from yogurt.types.json import JSONType


class APIRequest(BaseModel):
    method: str = Field(description="HTTP method, e.g. 'GET', 'POST', etc.")
    url: str
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    query_params: Optional[Dict[str, str]] = Field(default_factory=dict)
    body: Optional[Union[Dict[str, Any], List[Any], str]] = None  # handles JSON or raw


class APIResponse(BaseModel):
    status_code: int
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Any  # Can be JSON, text, or binary


class JSONResponse(BaseModel):
    status_code: int
    headers: Dict[str, str] = Field(default_factory=dict)
    json: JSONType
