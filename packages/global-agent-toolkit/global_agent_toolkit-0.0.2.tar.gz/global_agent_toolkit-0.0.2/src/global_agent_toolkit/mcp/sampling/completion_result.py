from typing import Literal

from src.cortex.genai.mcp.sampling.messages.image_message_content import (
    ImageMessageContent,
)
from src.cortex.genai.mcp.sampling.messages.text_message_content import (
    TextMessageContent,
)
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class CompletionResult(BaseModel):
    model: str = Field(description="Name of the model used")
    stopReason: Literal["endTurn", "stopSequence", "maxTokens"] | str | None = Field(
        default=None
    )
    role: Literal["user", "assistant"]
    content: TextMessageContent | ImageMessageContent = Field(discriminator="type")
