from src.infrastructure.decorators.value_objects import valueobject
from src.infrastructure.models.base_model import BaseModel
from src.infrastructure.models.field import Field


@valueobject
class QueryExpansion(BaseModel):
    expanded_query: str | None = Field(
        default=None,
        description="The expanded query. Or null.",
    )
