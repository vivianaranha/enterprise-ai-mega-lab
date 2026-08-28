from fastapi import APIRouter, Query
from backend.app.services.retrieval import retriever

router=APIRouter(prefix="/knowledge",tags=["Knowledge / RAG"])

@router.get("/search")
def search(q:str=Query(min_length=1),top_k:int=4):
    return retriever.search(q,top_k)
