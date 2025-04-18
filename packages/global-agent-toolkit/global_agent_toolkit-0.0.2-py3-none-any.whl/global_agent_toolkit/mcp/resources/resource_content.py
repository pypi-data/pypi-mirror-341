from src.infrastructure.models.base64str import Base64Str
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


class ResourceContent(BaseModel):
    uri: str
    mimeType: str | None = Field(default=None)
    text: str | None = Field(default=None)
    blob: Base64Str | None = Field(default=None)
