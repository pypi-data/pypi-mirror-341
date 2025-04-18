from __future__ import annotations

import abc

from src.cortex.genai.rag.documents.models.blob import Blob


class AsyncDownloadable[R = Blob](abc.ABC):
    @abc.abstractmethod
    async def download_async(self, uid: str) -> R: ...
