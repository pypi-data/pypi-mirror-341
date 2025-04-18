import abc

from src.cortex.genai.generations.guardrails.guardrail_validation_error import (
    GuardrailValidationError,
)
from src.infrastructure.containers.result import Result


class Guardrail(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, input: str) -> Result[None, GuardrailValidationError]: ...
