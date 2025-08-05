from pydantic import BaseModel
from typing import Dict, Any, Optional

from yogurt.documents import Document


class SearchResult(BaseModel):
    document: Document
    score: float


class RetrieverQuery(BaseModel):
    query_text: str
    filters: Optional[Dict[str, Any]] = None
