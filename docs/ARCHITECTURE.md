# Architecture

## Design goals

The lab is designed around five principles:

1. **Enterprise realism** — agents operate across multiple business domains.
2. **Local-first execution** — no paid model is required.
3. **Tool separation** — agents use enterprise tools rather than reading source files directly.
4. **Governed orchestration** — routing, tool scope, and approvals are explicit.
5. **Replaceable components** — mock systems can be swapped for real enterprise APIs.

## Runtime layers

### Experience layer

`frontend/app.py` provides a conversational Streamlit workspace.

### API layer

FastAPI exposes agent, data, RAG, and approval endpoints.

### Orchestration layer

The Enterprise Super Agent scores the user message against domain signals and selects one specialist agent. This intentionally deterministic baseline can later be replaced by LLM routing, a classifier, a graph workflow, or a planner.

### Specialist agents

Each specialist owns a bounded business responsibility and an allowlist of tools.

### Enterprise tool layer

`services/tools.py` provides stable methods such as `sales_opportunity_scores()` and `support_escalations()`. Real deployments can reimplement these methods with Salesforce, ServiceNow, Workday, SAP, Snowflake, custom APIs, or MCP servers.

### Data layer

CSV files are seed data. SQLite is the runtime store.

### Knowledge layer

Markdown files are indexed with TF-IDF. This provides a fully local RAG baseline with traceable source paths.

### Model layer

Ollama is optional. If unavailable, the system still completes core workflows using deterministic logic.
