from pydantic import BaseModel
from typing import Dict, Any, Optional


class YogurtError(BaseModel):
    error_type: str
    message: str
    stack: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
