from typing import Literal

from src.cortex.genai.mcp.sampling.messages.image_message_content import (
    ImageMessageContent,
)
from src.cortex.genai.mcp.sampling.messages.text_message_content import (
    TextMessageContent,
)
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class AssistantMessage(BaseModel):
    content: TextMessageContent | ImageMessageContent = Field(discriminator="type")
    role: Literal["assistant"] = Field(default="assistant")
