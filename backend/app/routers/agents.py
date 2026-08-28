from fastapi import APIRouter
from backend.app.schemas import AskRequest, AgentResponse
from backend.app.agents.super_agent import super_agent

router=APIRouter(prefix="/agents",tags=["Agents"])

@router.post("/ask",response_model=AgentResponse)
def ask_agent(req:AskRequest):
    return super_agent.ask(req.message,req.user_role)

@router.get("/catalog")
def catalog():
    return {
        "super_agent":"enterprise-super-agent",
        "agents":[
            {"name":name,"allowed_tools":agent.allowed_tools}
            for name,agent in super_agent.AGENTS.items()
        ]
    }
