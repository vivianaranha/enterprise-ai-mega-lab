from backend.app.agents.base import BaseAgent
from backend.app.schemas import AgentResponse, Source
from backend.app.services.retrieval import retriever
from backend.app.services.llm import llm

class KnowledgeAgent(BaseAgent):
    name="knowledge"
    allowed_tools=["knowledge"]

    def run(self,message:str,user_role:str="employee") -> AgentResponse:
        results=retriever.search(message)
        if not results:
            return AgentResponse(agent=self.name,intent="knowledge_search",answer="I could not find relevant material in the local knowledge base.")
        context="\n\n".join(f"SOURCE: {r['source']}\n{r['excerpt']}" for r in results)
        fallback="\n\n".join(r["excerpt"] for r in results[:2])
        answer=llm.generate(f"Answer the question using only the context below. Cite source file names in parentheses.\n\nQuestion: {message}\n\n{context}") or fallback
        return AgentResponse(agent=self.name,intent="knowledge_search",answer=answer,sources=[Source(**r) for r in results])

knowledge_agent=KnowledgeAgent()
