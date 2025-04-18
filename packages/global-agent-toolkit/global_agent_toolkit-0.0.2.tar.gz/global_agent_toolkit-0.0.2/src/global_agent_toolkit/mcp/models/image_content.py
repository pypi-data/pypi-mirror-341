from typing import Literal

from src.cortex.genai.mcp.models.annotations import Annotations
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.config_dict import ConfigDict
from src.infrastructure.models.field import Field


class ImageContent(BaseModel):
    """Image content for a message."""

    data: str
    """The base64-encoded image data."""
    mimeType: str
    """
    The MIME type of the image. Different providers may support different
    image types.
    """
    annotations: Annotations | None = None
    model_config = ConfigDict(extra="allow")

    type: Literal["image"] = Field(default="image")
