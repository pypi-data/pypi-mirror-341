from cerebras.cloud.sdk.types.chat.completion_create_params import (
    MessageAssistantMessageRequestTyped,
    MessageSystemMessageRequestTyped,
    MessageUserMessageRequestTyped,
)

from src.cortex.genai.generations.models.assistant_message import AssistantMessage
from src.cortex.genai.generations.models.developer_message import DeveloperMessage
from src.cortex.genai.generations.models.user_message import UserMessage
from src.infrastructure.adapters import Adapter


class CortexMessageToCerebrasMessageAdapter(
    Adapter[
        AssistantMessage | DeveloperMessage | UserMessage,
        MessageSystemMessageRequestTyped
        | MessageAssistantMessageRequestTyped
        | MessageUserMessageRequestTyped,
    ]
):
    def adapt(
        self, _f: AssistantMessage | DeveloperMessage | UserMessage
    ) -> (
        MessageSystemMessageRequestTyped
        | MessageAssistantMessageRequestTyped
        | MessageUserMessageRequestTyped
    ):
        match _f:
            case AssistantMessage():
                return MessageAssistantMessageRequestTyped(
                    role="assistant", content="".join(p.text for p in _f.parts)
                )
            case DeveloperMessage():
                return MessageSystemMessageRequestTyped(
                    role="system", content="".join(p.text for p in _f.parts)
                )
            case UserMessage():
                return MessageUserMessageRequestTyped(
                    role="user", content="".join(p.text for p in _f.parts)
                )
