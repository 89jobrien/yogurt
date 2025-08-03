from abc import ABC, abstractmethod
from typing import List
from yogurt.documents.base import Document

class BaseTextSplitter(ABC):
    """Interface for splitting text into smaller chunks."""
    @abstractmethod
    def split_documents(self, documents: List[Document]) -> List[Document]:
        pass