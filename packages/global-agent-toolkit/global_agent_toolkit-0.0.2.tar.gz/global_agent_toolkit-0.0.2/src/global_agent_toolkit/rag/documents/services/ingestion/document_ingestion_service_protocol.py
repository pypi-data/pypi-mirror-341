from __future__ import annotations

from abc import abstractmethod
from pathlib import Path

from src.infrastructure.contracts.repositories.writable import AsyncWritable
from src.infrastructure.coroutines.run_sync import run_sync
from src.infrastructure.decorators.services import abstractservice


@abstractservice
class DocumentIngestionServiceProtocol:
    writable_repository: AsyncWritable[Path]

    def __init__(self, writable_repository: AsyncWritable[Path]) -> None:
        self.writable_repository = writable_repository

    def create_document(self, file_path: str) -> None:
        return run_sync(self.create_document_async, file_path=file_path)

    @abstractmethod
    async def create_document_async(self, file_path: str) -> None: ...
