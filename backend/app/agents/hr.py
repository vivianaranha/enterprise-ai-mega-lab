from collections import Counter
from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse, Source
from backend.app.services.tools import tools
from backend.app.services.retrieval import retriever

class HRAgent(BaseAgent):
    name="hr"
    allowed_tools=["employees","knowledge"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        m=message.lower()
        if any(k in m for k in ["policy","travel","expense","remote","hybrid"]):
            results=retriever.search(message)
            answer=(results[0]["excerpt"] if results else "No relevant HR policy was found.")
            return AgentResponse(agent=self.name,intent="hr_policy_qa",answer=answer,sources=[Source(**r) for r in results])
        employees=tools.employees()
        depts=Counter(e["department"] for e in employees)
        answer="Workforce snapshot: " + ", ".join(f"{d}: {n}" for d,n in sorted(depts.items())) + "."
        return AgentResponse(agent=self.name,intent="workforce_insight",answer=answer,data=employees,recommended_actions=["Use aggregated workforce data for planning; avoid consequential decisions based solely on automated analysis."])

hr_agent=HRAgent()
