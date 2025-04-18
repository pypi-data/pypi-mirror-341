from collections.abc import Sequence

from src.cortex.genai.mcp.models.embedded_resource import EmbeddedResource
from src.cortex.genai.mcp.models.image_content import ImageContent
from src.cortex.genai.mcp.models.text_content import TextContent
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class CallToolResult(BaseModel):
    """The server's response to a tool call."""

    metadata: dict[str, object] = Field(default_factory=dict)
    content: Sequence[TextContent | ImageContent | EmbeddedResource]
    isError: bool = Field(default=False)
