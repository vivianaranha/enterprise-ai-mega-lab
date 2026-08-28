from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse
from backend.app.services.tools import tools

class SalesAgent(BaseAgent):
    name = "sales"
    allowed_tools = ["accounts", "contacts", "opportunities", "tickets", "meetings"]

    def run(self, message: str, user_role: str = "employee") -> AgentResponse:
        m = message.lower()
        # Account-specific context
        target = next((a for a in tools.accounts() if a["name"].lower() in m), None)
        if target:
            ctx = tools.account_context(target["account_id"])
            if any(k in m for k in ["who", "contact", "stakeholder", "reach out"]):
                contacts = sorted(ctx["contacts"], key=lambda c: (c["influence"] != "High", c["relationship"] == "Cold"))
                answer = f"For {target['name']}, I found {len(contacts)} CRM contacts. Start with " + ", ".join(f"{c['name']} ({c['title']})" for c in contacts[:3]) + "."
                return AgentResponse(agent=self.name,intent="stakeholder_identification",answer=answer,data=contacts,recommended_actions=["Confirm the business objective for each stakeholder", "Tailor outreach to the modernization trigger"])
            if any(k in m for k in ["meeting", "prepare", "brief"]):
                open_tickets=[t for t in ctx["tickets"] if t["status"]=="Open"]
                answer=(f"Meeting brief for {target['name']}: growth signal: {target['growth_signal']}. "
                        f"There are {len(ctx['opportunities'])} active opportunities and {len(open_tickets)} open support tickets. "
                        f"Customer health is {target['health']}.")
                actions=[o["next_step"] for o in ctx["opportunities"][:2]] or ["Clarify the customer's top business priority"]
                return AgentResponse(agent=self.name,intent="meeting_preparation",answer=answer,data=ctx,recommended_actions=actions)

        scored = tools.sales_opportunity_scores()
        top=scored[:5]
        answer="Top sales priorities: " + "; ".join(f"{r['account_name']} – {r['name']} (score {r['priority_score']})" for r in top) + "."
        return AgentResponse(agent=self.name,intent="opportunity_prioritization",answer=answer,data=top,recommended_actions=[f"{r['account_name']}: {r['next_step']}" for r in top[:3]])

sales_agent = SalesAgent()
