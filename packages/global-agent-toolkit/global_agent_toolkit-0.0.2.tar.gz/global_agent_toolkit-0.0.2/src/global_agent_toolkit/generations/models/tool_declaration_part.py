from typing import Literal
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class ToolDeclarationPart(BaseModel):
    type: Literal["tool_declaration"] = Field(default="tool_declaration")
    name: str
