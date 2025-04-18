from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class ResourceDescription(BaseModel):
    uri: str
    name: str
    description: str | None = Field(default=None)
    mimeType: str | None = Field(default=None)
