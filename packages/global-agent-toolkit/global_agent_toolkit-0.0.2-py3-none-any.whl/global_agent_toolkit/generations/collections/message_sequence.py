from __future__ import annotations

from src.cortex.genai.generations.models.developer_message import DeveloperMessage
from src.cortex.genai.generations.models.message import Message
from src.infrastructure.collections.readonly_collection import ReadonlyCollection


class MessageSequence(ReadonlyCollection[Message]):
    def append(self, messages: list[Message]) -> MessageSequence:
        return MessageSequence(elements=list(self.elements) + list(messages))

    def without_developer_prompt(self) -> MessageSequence:
        return MessageSequence(
            list(
                filter(
                    lambda message: not isinstance(message, DeveloperMessage),
                    self.elements,
                )
            )
        )
