from abc import ABC, abstractmethod

from yogurt.documents.base import DocumentList


class BaseVectorStore(ABC):
    """Interface for storing and retrieving embedded documents."""

    @abstractmethod
    def add_documents(self, documents: DocumentList) -> None:
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> DocumentList | None:
        pass
