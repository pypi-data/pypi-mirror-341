from typing import Annotated

from src.infrastructure.models.any_url import AnyUrl
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.config_dict import ConfigDict
from src.infrastructure.models.url_constraints import UrlConstraints


class ResourceContents(BaseModel):
    """The contents of a specific resource or sub-resource."""

    uri: Annotated[AnyUrl, UrlConstraints(host_required=False)]
    """The URI of this resource."""
    mimeType: str | None = None
    """The MIME type of this resource, if known."""
    model_config = ConfigDict(extra="allow")
