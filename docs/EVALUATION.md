# Agent Evaluation

A useful enterprise agent evaluation suite should score more than answer quality.

## Suggested dimensions

- Router accuracy
- Tool selection accuracy
- Entity resolution accuracy
- Groundedness
- Citation correctness
- Task completion
- Policy compliance
- Refusal / escalation correctness
- Latency
- Reliability when dependencies fail

## Starter test set

| Prompt | Expected agent |
| --- | --- |
| Find the best opportunities | sales |
| Which critical tickets are open? | support |
| What is our travel policy? | hr or knowledge |
| Explain finance variances | finance |
| Which SKUs might stock out? | operations |
| Give me a cross-functional executive brief | executive |

The automated tests include deterministic router and tool checks. Extend them with golden datasets and model-based evaluations if you enable a generative model.
