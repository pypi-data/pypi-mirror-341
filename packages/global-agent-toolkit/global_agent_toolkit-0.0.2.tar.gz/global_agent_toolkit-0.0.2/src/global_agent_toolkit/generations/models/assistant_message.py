from typing import Literal, Sequence

from src.cortex.genai.generations.models.file_part import FilePart
from src.cortex.genai.generations.models.text_part import TextPart
from src.cortex.genai.generations.models.tool_execution_part import ToolExecutionPart
from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class AssistantMessage(BaseModel):
    parts: Sequence[TextPart | FilePart | ToolExecutionPart]
    role: Literal["assistant"] = Field(default="assistant")
