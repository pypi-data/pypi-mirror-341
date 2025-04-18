from typing import Literal

from src.cortex.genai.mcp.models.annotations import Annotations
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.config_dict import ConfigDict
from src.infrastructure.models.field import Field


class TextContent(BaseModel):
    """Text content for a message."""

    type: Literal["text"] = Field(default="text")
    text: str
    """The text content of the message."""
    annotations: Annotations | None = None
    model_config = ConfigDict(extra="allow")
