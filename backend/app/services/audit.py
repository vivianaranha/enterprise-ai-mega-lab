from datetime import datetime, timezone
from backend.app.services.database import db

def log_agent_request(user_role: str, message: str, selected_agent: str, intent: str, metadata: dict):
    db.insert_audit(
        datetime.now(timezone.utc).isoformat(),
        user_role,
        message,
        selected_agent,
        intent,
        metadata,
    )
