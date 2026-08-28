from datetime import datetime, timezone
from fastapi import APIRouter
from backend.app.schemas import ApprovalRequest
from backend.app.services.database import db

router=APIRouter(prefix="/approvals",tags=["Human Approval"])

@router.post("")
def create_approval(req:ApprovalRequest):
    approval_id=db.create_approval(datetime.now(timezone.utc).isoformat(),req.action,req.entity_type,req.entity_id,req.proposed_change,req.reason)
    return {"approval_id":approval_id,"status":"pending","message":"No enterprise write was executed. This lab records the proposal for human review."}
