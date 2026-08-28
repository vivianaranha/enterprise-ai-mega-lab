from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    message: str = Field(min_length=1)
    user_role: str = "employee"
    conversation_id: Optional[str] = None

class Source(BaseModel):
    source: str
    score: float | None = None
    excerpt: str | None = None

class AgentResponse(BaseModel):
    agent: str
    intent: str
    answer: str
    data: Any = None
    recommended_actions: List[str] = Field(default_factory=list)
    sources: List[Source] = Field(default_factory=list)
    requires_approval: bool = False
    trace: Dict[str, Any] = Field(default_factory=dict)

class EntityRecord(BaseModel):
    resource: str
    data: Dict[str, Any]

class ApprovalRequest(BaseModel):
    action: str
    entity_type: str
    entity_id: str
    proposed_change: Dict[str, Any]
    reason: str
