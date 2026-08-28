from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse
from backend.app.services.tools import tools

class OperationsAgent(BaseAgent):
    name="operations"
    allowed_tools=["inventory","shipments"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        risks=tools.inventory_risks()
        shipments=tools.shipments()
        high=[r for r in risks if r["risk"]=="High"]
        delayed=[s for s in shipments if s["status"]=="Delayed"]
        answer=f"Operations risk: {len(high)} high-risk inventory item(s) and {len(delayed)} delayed shipment(s)."
        actions=[f"Replenish {r['item']} ({r['sku']}): {r['weeks_of_supply']} weeks of supply, {r['lead_time_days']:.0f}-day lead time" for r in high]
        actions += [f"Escalate shipment {s['shipment_id']} from {s['supplier']} ({s['days_late']:.0f} days late)" for s in delayed]
        return AgentResponse(agent=self.name,intent="operations_risk",answer=answer,data={"inventory":risks,"shipments":shipments},recommended_actions=actions)

operations_agent=OperationsAgent()
