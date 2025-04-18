from collections.abc import Sequence
from typing import Literal

from src.cortex.genai.generations.models.file_part import FilePart
from src.cortex.genai.generations.models.text_part import TextPart
from src.cortex.genai.generations.models.tool_declaration_part import (
    ToolDeclarationPart,
)
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class UserMessage(BaseModel):
    parts: Sequence[TextPart | FilePart | ToolDeclarationPart]
    role: Literal["user"] = Field(default="user")
