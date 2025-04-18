from collections.abc import Sequence
from typing import Literal

from src.cortex.genai.generations.models.part import Part
from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class GeneratedAssistantMessage[T](BaseModel):
    parts: Sequence[Part]
    parsed: T
    role: Literal["assistant"] = Field(default="assistant")

    @property
    def text(self) -> str:
        return "".join(part.text for part in self.parts)
