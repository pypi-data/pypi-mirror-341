from src.cortex.genai.mcp.tools.input_schema import InputSchema
from src.infrastructure.models.base_model import BaseModel


class Tool(BaseModel):
    """Definition for a tool the client can call."""

    name: str
    """The name of the tool."""
    description: str | None = None
    """A human-readable description of the tool."""
    inputSchema: InputSchema
    """A JSON Schema object defining the expected parameters for the tool."""
