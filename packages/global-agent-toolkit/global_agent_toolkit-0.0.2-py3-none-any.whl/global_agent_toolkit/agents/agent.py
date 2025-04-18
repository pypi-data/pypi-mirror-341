from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from src.cortex.genai.agents.agent_config import AgentConfig
from src.cortex.genai.agents.agent_instructions import AgentInstructions
from src.cortex.genai.agents.agent_run_response import AgentRunResponse
from src.cortex.genai.agents.models.context import Context
from src.cortex.genai.agents.pipelines.agent_pipeline import AgenticPipeline
from src.cortex.genai.agents.squads.agent_squad import AgentSquad
from src.cortex.genai.generations.models.message import Message
from src.cortex.genai.generations.models.part import Part
from src.cortex.genai.generations.models.user_message import UserMessage
from src.cortex.genai.generations.providers.base.generation_provider import (
    GenerationProvider,
)
from src.cortex.genai.generations.tools.tool import Tool as GenerationTool
from src.cortex.genai.mcp.servers.mcp_server import MCPServer
from src.cortex.genai.mcp.tools.mcp_tool import Tool as MCPTool
from src.infrastructure.coroutines.run_sync import run_sync
from src.infrastructure.models.base_model import BaseModel


class Agent[T = str](BaseModel):
    name: str
    description: str
    instructions: (
        str
        | Callable[[], str]
        | Callable[[Context], str]
        | Sequence[str]
        | AgentInstructions
    )
    response_schema: type[T]
    generation_provider: GenerationProvider
    model: str
    mcp_servers: Sequence[MCPServer]
    tools: Sequence[Callable[..., object] | GenerationTool | MCPTool]
    config: AgentConfig

    def run(
        self,
        input: str
        | Context
        | Sequence[Message]
        | UserMessage
        | Part
        | Sequence[Part]
        | Callable[[], str],
    ) -> AgentRunResponse[T]:
        return run_sync(self.run_async, input=input)

    async def run_async(
        self,
        input: str
        | Context
        | Sequence[Message]
        | UserMessage
        | Part
        | Sequence[Part]
        | Callable[[], str]
        | Callable[[Context], str],
    ) -> AgentRunResponse[T]: ...

    def __add__(self, other: Agent[Any]) -> AgentSquad: ...

    def __or__(self, other: Agent) -> AgenticPipeline: ...
