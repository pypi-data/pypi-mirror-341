from collections.abc import Sequence
from typing import Literal

from src.cortex.genai.generations.models.part import Part
from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class RawPartsResponse(BaseModel):
    raw_parts: Sequence[Part] = Field(description="Just the raw LLM output.")

    def __bool__(self) -> Literal[False]:
        return False
