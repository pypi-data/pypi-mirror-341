from typing import override

from src.cortex.genai.rag.documents.models.document import Document
from src.infrastructure.contracts.repositories.readable import AsyncReader


class MilvusRagDocumentRepository(AsyncReader[Document, str]):
    @override
    async def read(
        self, uid: str, filters: dict[str, object] | None = None
    ) -> Document: ...
