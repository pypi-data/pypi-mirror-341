from typing import Literal

from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class TextMessageContent(BaseModel):
    text: str | None = Field(description="text of the message")
    type: Literal["text"] = Field(default="text")
