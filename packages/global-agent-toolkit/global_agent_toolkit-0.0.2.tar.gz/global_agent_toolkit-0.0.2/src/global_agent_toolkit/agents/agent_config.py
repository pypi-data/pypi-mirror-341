from src.cortex.genai.generations.models.generation_config import GenerationConfig
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class AgentConfig(BaseModel):
    generation_config: GenerationConfig
    max_tool_calls: int = Field(default=15)
    max_iterations: int = Field(default=20)
