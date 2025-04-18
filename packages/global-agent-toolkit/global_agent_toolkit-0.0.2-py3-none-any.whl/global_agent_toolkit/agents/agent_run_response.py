from src.infrastructure.models.base_model import BaseModel


class AgentRunResponse[T](BaseModel):
    response: T
