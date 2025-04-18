from typing import Literal

from src.cortex.genai.mcp.models.resource_contents import ResourceContents
from src.infrastructure.models.field import Field


class BlobResourceContents(ResourceContents):
    """Binary contents of a resource."""

    type: Literal["blob"] = Field(default="blob")

    blob: str
    """A base64-encoded string representing the binary data of the item."""
