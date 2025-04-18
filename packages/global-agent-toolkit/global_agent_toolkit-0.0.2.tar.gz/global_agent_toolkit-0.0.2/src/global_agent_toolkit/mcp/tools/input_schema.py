from typing import Literal

from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class InputSchema(BaseModel):
    properties: dict[str, object] = Field(description="Tool specific parameters")
    type: Literal["object"] = Field(default="object")
