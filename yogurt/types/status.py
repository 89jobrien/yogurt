from pydantic import BaseModel
from typing import Literal, Optional, Any


class OperationStatus(BaseModel):
    code: Literal["success", "error", "pending"]
    message: Optional[str] = None
    detail: Optional[Any] = None
