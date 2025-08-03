from abc import ABC, abstractmethod
from typing import List
from yogurt.documents import Document

class BaseDocumentLoader(ABC):
    """Interface for loading Documents from a source."""
    @abstractmethod
    def load(self) -> List[Document]:
        pass