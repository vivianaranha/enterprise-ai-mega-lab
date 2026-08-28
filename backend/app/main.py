from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.config import settings
from backend.app.services.database import db
from backend.app.routers import agents, data, knowledge, approvals

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.ensure_seeded()
    yield

app=FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Local-first enterprise AI sandbox with specialist agents, RAG, tool use, and governance patterns.",
    lifespan=lifespan,
)

app.include_router(agents.router)
app.include_router(data.router)
app.include_router(knowledge.router)
app.include_router(approvals.router)

@app.get("/")
def root():
    return {
        "name":settings.app_name,
        "status":"ready",
        "docs":"/docs",
        "agent_endpoint":"POST /agents/ask",
    }

@app.get("/health")
def health(): return {"status":"ok"}
