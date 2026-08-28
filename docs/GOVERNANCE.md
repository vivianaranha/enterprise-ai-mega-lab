# AI Governance

This repository treats governance as an architecture concern, not a final checklist.

## Controls demonstrated

- Agent tool allowlists
- Read-only enterprise access by default
- Explicit approval object for write proposals
- Audit records for routed user requests
- Source citations for knowledge retrieval
- Deterministic fallback when the LLM is unavailable
- Bounded specialist responsibilities
- Human review guidance for consequential workforce decisions

## Production additions

A production implementation should add identity, role-based access, secrets management, environment separation, model/version inventory, evaluation gates, data classification, retention controls, approval workflows, monitoring, incident response, and formal risk assessments.

## Human-in-the-loop pattern

High-impact actions should follow:

`Agent recommendation → proposed change → human review → policy check → enterprise write → verification → audit`

The included `/approvals` endpoint implements the first two steps only.
