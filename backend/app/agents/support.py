from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse
from backend.app.services.tools import tools

class SupportAgent(BaseAgent):
    name="support"
    allowed_tools=["tickets","accounts"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        escalations=tools.support_escalations()
        critical=[e for e in escalations if e["severity"]=="Critical"]
        answer=f"I found {len(escalations)} open tickets that warrant escalation or close review, including {len(critical)} critical incident(s)."
        actions=[]
        for e in escalations[:5]:
            why=[]
            if e["severity"]=="Critical": why.append("critical severity")
            if e["sla_breached"]: why.append("SLA breached")
            if e["sentiment"] in {"Negative","Frustrated"}: why.append("negative customer sentiment")
            actions.append(f"{e['ticket_id']} / {e['account_name']}: escalate because {', '.join(why)}")
        return AgentResponse(agent=self.name,intent="support_escalation",answer=answer,data=escalations,recommended_actions=actions)

support_agent=SupportAgent()
