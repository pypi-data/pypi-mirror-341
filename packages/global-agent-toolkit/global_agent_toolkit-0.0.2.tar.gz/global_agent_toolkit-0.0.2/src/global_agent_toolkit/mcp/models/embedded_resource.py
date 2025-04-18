from typing import Literal

from src.cortex.genai.mcp.models.annotations import Annotations
from src.cortex.genai.mcp.models.blob_resource_contents import BlobResourceContents
from src.cortex.genai.mcp.models.text_resource_contents import TextResourceContents
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.config_dict import ConfigDict
from src.infrastructure.models.field import Field


class EmbeddedResource(BaseModel):
    """
    The contents of a resource, embedded into a prompt or tool call result.

    It is up to the client how best to render embedded resources for the benefit
    of the LLM and/or the user.
    """

    type: Literal["resource"] = Field(default="resource")
    resource: TextResourceContents | BlobResourceContents = Field(discriminator="type")
    annotations: Annotations | None = None
    model_config = ConfigDict(extra="allow")
