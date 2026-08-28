from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse
from backend.app.services.tools import tools

class ExecutiveAgent(BaseAgent):
    name="executive"
    allowed_tools=["accounts","opportunities","tickets","finance","inventory","shipments"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        support=tools.support_escalations()
        sales=tools.sales_opportunity_scores()
        finance=[r for r in tools.finance_variances() if r["needs_review"]]
        inventory=[r for r in tools.inventory_risks() if r["risk"]=="High"]
        answer=(f"Executive brief: {len(support)} support issue(s) need escalation, "
                f"{len(finance)} department(s) exceed finance variance thresholds, and {len(inventory)} inventory item(s) are high risk. "
                f"The highest-priority sales opportunity is {sales[0]['account_name']} / {sales[0]['name']}.")
        actions=[]
        if support: actions.append(f"Review support escalation at {support[0]['account_name']} ({support[0]['ticket_id']}).")
        if sales: actions.append(f"Advance {sales[0]['account_name']}: {sales[0]['next_step']}.")
        if finance: actions.append(f"Investigate {finance[0]['department']} spend variance.")
        if inventory: actions.append(f"Mitigate stockout risk for {inventory[0]['item']}.")
        return AgentResponse(agent=self.name,intent="executive_briefing",answer=answer,data={"support":support,"sales":sales[:3],"finance":finance,"inventory":inventory},recommended_actions=actions)

executive_agent=ExecutiveAgent()
