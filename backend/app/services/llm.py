import requests
from backend.app.config import settings

class LocalLLM:
    def available(self) -> bool:
        if not settings.use_ollama:
            return False
        try:
            r = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=1.5)
            return r.ok
        except requests.RequestException:
            return False

    def generate(self, prompt: str, system: str = "You are a concise enterprise AI assistant.") -> str | None:
        if not self.available():
            return None
        try:
            r = requests.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()["message"]["content"]
        except Exception:
            return None

llm = LocalLLM()
