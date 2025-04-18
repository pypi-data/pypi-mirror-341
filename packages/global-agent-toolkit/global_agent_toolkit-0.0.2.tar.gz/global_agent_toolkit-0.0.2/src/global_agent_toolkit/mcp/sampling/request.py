from typing import Literal, Sequence

from src.cortex.genai.generations.models.user_message import UserMessage
from src.cortex.genai.mcp.sampling.messages.assistant_message import AssistantMessage
from src.cortex.genai.mcp.sampling.model_preferences import ModelPreference
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class SamplingRequest(BaseModel):
    messages: Sequence[AssistantMessage | UserMessage] = Field(discriminator="role")
    modelPreferences: ModelPreference | None = Field(default=None)
    systemPrompt: str | None = Field(default=None)
    includeContext: Literal["none", "thisServer", "allServers"] | None = Field(
        default=None
    )
    temperature: float | None = Field(default=None, ge=0.0, le=1.0)
    maxTokens: float
    stopSequences: Sequence[str] | None = Field(default=None)
    metadata: dict[str, object] = Field(default_factory=dict)
