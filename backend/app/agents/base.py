from abc import ABC, abstractmethod
from backend.app.schemas import AgentResponse
from backend.app.services.llm import llm

class BaseAgent(ABC):
    name = "base"
    allowed_tools: list[str] = []

    @abstractmethod
    def run(self, message: str, user_role: str = "employee") -> AgentResponse:
        raise NotImplementedError

    def maybe_polish(self, prompt: str, fallback: str) -> str:
        generated = llm.generate(prompt)
        return generated.strip() if generated else fallback
