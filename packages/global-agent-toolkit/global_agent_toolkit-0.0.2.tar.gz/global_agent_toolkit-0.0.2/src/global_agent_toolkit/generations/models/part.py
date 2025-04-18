from typing import Annotated

from src.cortex.genai.generations.models.file_part import FilePart
from src.cortex.genai.generations.models.text_part import TextPart
from src.infrastructure.models.field import Field

type Part = Annotated[TextPart | FilePart, Field(discriminator="type")]
