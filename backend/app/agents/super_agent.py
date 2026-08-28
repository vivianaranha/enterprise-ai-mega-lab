import re
from backend.app.schemas import AgentResponse
from backend.app.agents.sales import sales_agent
from backend.app.agents.support import support_agent
from backend.app.agents.hr import hr_agent
from backend.app.agents.finance import finance_agent
from backend.app.agents.operations import operations_agent
from backend.app.agents.executive import executive_agent
from backend.app.agents.knowledge import knowledge_agent
from backend.app.services.audit import log_agent_request

class EnterpriseSuperAgent:
    name="enterprise-super-agent"

    ROUTES = {
        "sales": ["sales", "lead", "opportunity", "pipeline", "account", "stakeholder", "contact", "meeting", "customer", "crm", "reach out"],
        "support": ["support", "ticket", "incident", "sla", "escalat", "service issue"],
        "hr": ["employee", "workforce", "talent", "hr", "travel", "reimbursement", "expense policy", "remote work", "hybrid"],
        "finance": ["finance", "budget", "variance", "spend", "forecast", "cost"],
        "operations": ["inventory", "shipment", "supplier", "stockout", "supply chain", "warehouse", "operations"],
        "executive": ["executive", "leadership", "briefing", "what should i know", "top risks", "across the business"],
        "knowledge": ["policy", "what is", "how do", "documentation", "knowledge", "secure edge", "cloud connect", "ai ops"],
    }

    AGENTS = {
        "sales": sales_agent,
        "support": support_agent,
        "hr": hr_agent,
        "finance": finance_agent,
        "operations": operations_agent,
        "executive": executive_agent,
        "knowledge": knowledge_agent,
    }

    def route(self, message: str) -> tuple[str, dict]:
        m=message.lower()
        scores={name:sum(1 for keyword in kws if keyword in m) for name,kws in self.ROUTES.items()}
        # Executive phrasing should override domain ties when a cross-functional summary is requested.
        if any(k in m for k in ["executive brief", "across the business", "top risks", "what should i know today"]):
            scores["executive"] += 5
        selected=max(scores,key=scores.get)
        if scores[selected] == 0:
            selected="knowledge"
        return selected, scores

    def ask(self, message: str, user_role: str = "employee") -> AgentResponse:
        selected, scores=self.route(message)
        response=self.AGENTS[selected].run(message,user_role)
        response.trace={"router":self.name,"selected_agent":selected,"route_scores":scores,"allowed_tools":self.AGENTS[selected].allowed_tools}
        log_agent_request(user_role,message,selected,response.intent,response.trace)
        return response

super_agent=EnterpriseSuperAgent()
