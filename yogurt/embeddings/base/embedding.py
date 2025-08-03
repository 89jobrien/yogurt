from typing import List, TypeAlias

# Embedding for a single document/query
Embedding: TypeAlias = List[float]

# Embeddings for multiple documents/queries
Embeddings: TypeAlias = List[Embedding]