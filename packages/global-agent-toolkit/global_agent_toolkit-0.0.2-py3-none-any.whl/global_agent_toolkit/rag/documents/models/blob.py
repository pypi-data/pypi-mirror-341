from __future__ import annotations

from dataclasses import dataclass

from src.infrastructure.decorators.value_objects import valueobject


@dataclass(frozen=True)
@valueobject
class Blob:
    data: bytes
    extension: str
