from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class PromptArgument(BaseModel):
    name: str
    description: str | None = Field(default=None)
    required: bool | None = Field(default=None)
