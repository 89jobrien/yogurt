from abc import ABC, abstractmethod
from typing import List, TypeAlias

Embedding: TypeAlias = List[float]
Embeddings: TypeAlias = List[Embedding]


class BaseEmbedder(ABC):
    """Interface for creating vector embeddings of text."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> Embeddings:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> Embedding:
        pass
