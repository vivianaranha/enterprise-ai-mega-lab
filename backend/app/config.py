from dataclasses import dataclass
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Enterprise AI Mega Lab")
    database_path: str = os.getenv("DATABASE_PATH", "enterprise.db")
    use_ollama: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    top_k_retrieval: int = int(os.getenv("TOP_K_RETRIEVAL", "4"))
    project_root: Path = Path(__file__).resolve().parents[2]

settings = Settings()
