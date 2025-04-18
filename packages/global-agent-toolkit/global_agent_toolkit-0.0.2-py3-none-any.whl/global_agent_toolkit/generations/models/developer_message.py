from typing import Literal, Sequence

from src.cortex.genai.generations.models.part import Part
from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class DeveloperMessage(BaseModel):
    parts: Sequence[Part]
    role: Literal["developer"] = Field(default="developer")
