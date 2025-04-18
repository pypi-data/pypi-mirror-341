from typing import Annotated

from src.cortex.genai.generations.models.assistant_message import AssistantMessage
from src.cortex.genai.generations.models.developer_message import DeveloperMessage
from src.cortex.genai.generations.models.user_message import UserMessage
from src.infrastructure.models.field import Field

type Message = Annotated[
    AssistantMessage | DeveloperMessage | UserMessage, Field(discriminator="role")
]
