# Security

## Threats to consider

- Prompt injection from documents or external content
- Excessive agent permissions
- Data leakage to external model providers
- Tool argument manipulation
- Cross-tenant data access
- Sensitive fields in logs
- Hallucinated write actions
- Poisoned knowledge sources

## Baseline defenses in this lab

- No write-capable enterprise tools are exposed to agents by default.
- Specialist agents declare explicit tool allowlists.
- Knowledge answers expose source paths.
- Ollama is optional and local.
- The Responsible AI Use Policy is part of the knowledge base.

## Production hardening

Use SSO, RBAC/ABAC, secrets vaults, signed tool requests, network egress controls, schema validation, content classification, encrypted storage, trace redaction, security testing, and scoped service identities for every connector.
