from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class Hint(BaseModel):
    name: str | None = Field(default=None)
