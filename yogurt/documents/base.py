from typing import List, Dict, Any, TypeAlias
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


DocumentType: TypeAlias = Document
DocumentList: TypeAlias = List[Document]
