from src.cortex.genai.generations.models.generated_assistant_message import (
    GeneratedAssistantMessage,
)
from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class Choice[T](BaseModel):
    index: int = Field(description="The index of the choice.")

    message: GeneratedAssistantMessage[T] = Field(
        description="The message of the Choice.", kw_only=False
    )
