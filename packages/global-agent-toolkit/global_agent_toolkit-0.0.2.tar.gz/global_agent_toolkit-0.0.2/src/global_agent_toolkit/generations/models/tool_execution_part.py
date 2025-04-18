from typing import Literal
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class ToolExecutionPart(BaseModel):
    type: Literal["tool_execution"] = Field(
        default="tool_execution",
    )
    tool_name: str
    args: dict[str, object] = Field(default_factory=dict)
