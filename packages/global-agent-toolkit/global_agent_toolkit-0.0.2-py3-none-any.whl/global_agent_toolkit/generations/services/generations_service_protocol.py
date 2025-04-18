from __future__ import annotations

import abc
from collections.abc import Sequence

from src.cortex.genai.generations.models.generation import Generation
from src.cortex.genai.generations.models.message import Message
from src.cortex.genai.generations.models.raw_parts_response import RawPartsResponse
from src.cortex.genai.generations.providers import GenerationProvider
from src.infrastructure.coroutines.run_sync import run_sync
from src.infrastructure.decorators.services import abstractservice


@abstractservice
class GenerationsServiceProtocol(abc.ABC):
    generation_provider: GenerationProvider

    def __init__(
        self,
        generation_strategy: GenerationProvider,
    ) -> None:
        self.generation_provider = generation_strategy

    def generate[T = RawPartsResponse](
        self,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
    ) -> Generation[T]:
        return run_sync(
            self.generate_async,
            model=model,
            messages=messages,
            response_schema=response_schema,
        )

    @abc.abstractmethod
    async def generate_async[T = RawPartsResponse](
        self,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
    ) -> Generation[T]: ...
