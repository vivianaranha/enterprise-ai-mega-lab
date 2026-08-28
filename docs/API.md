# API Guide

## Health

`GET /health`

## Ask the Super Agent

`POST /agents/ask`

```json
{
  "message": "Which support tickets need immediate escalation?",
  "user_role": "manager"
}
```

The response includes the selected specialist, intent, answer, structured data, recommended actions, source citations when applicable, and routing trace.

## Agent catalog

`GET /agents/catalog`

## Enterprise data

- `GET /data/resources`
- `GET /data/{resource}`
- `GET /data/{resource}/{entity_id}`

Supported resources: accounts, contacts, opportunities, tickets, employees, finance, inventory, shipments, meetings.

## Knowledge retrieval

`GET /knowledge/search?q=travel+reimbursement&top_k=4`

## Human approval placeholder

`POST /approvals`

This endpoint records a proposed write action but deliberately does not execute the underlying enterprise change.
