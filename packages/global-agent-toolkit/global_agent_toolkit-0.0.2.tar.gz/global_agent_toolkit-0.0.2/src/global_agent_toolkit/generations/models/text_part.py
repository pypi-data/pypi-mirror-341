from typing import Literal

from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class TextPart(BaseModel):
    text: str
    type: Literal["text"] = Field(default="text")
