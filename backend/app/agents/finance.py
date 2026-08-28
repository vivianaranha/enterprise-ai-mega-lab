from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse
from backend.app.services.tools import tools

class FinanceAgent(BaseAgent):
    name="finance"
    allowed_tools=["finance"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        rows=tools.finance_variances()
        review=[r for r in rows if r["needs_review"]]
        answer=f"{len(review)} departments exceed the variance review threshold. The largest unfavorable variance is {rows[0]['department']} at ${rows[0]['variance_k']:.0f}K ({rows[0]['variance_pct']:.1f}%)."
        actions=[f"{r['department']}: investigate ${r['variance_k']:.0f}K / {r['variance_pct']:.1f}% variance and update forecast assumptions" for r in review]
        return AgentResponse(agent=self.name,intent="finance_variance_analysis",answer=answer,data=rows,recommended_actions=actions)

finance_agent=FinanceAgent()
