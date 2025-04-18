from collections.abc import Sequence

from src.cortex.genai.mcp.prompts.prompt_argument import PromptArgument
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class Prompt(BaseModel):
    name: str
    description: str | None = Field(default=None)
    arguments: Sequence[PromptArgument]
