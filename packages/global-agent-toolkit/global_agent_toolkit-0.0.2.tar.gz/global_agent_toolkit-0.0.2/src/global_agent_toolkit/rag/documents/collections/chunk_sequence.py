from __future__ import annotations

from src.cortex.genai.rag.documents.models.chunk import Chunk
from src.infrastructure.collections.readonly_collection import ReadonlyCollection


class ChunkSequence(ReadonlyCollection[Chunk]):
    def describe(self) -> str:
        return "".join(chunk.describe() for chunk in self.elements)
