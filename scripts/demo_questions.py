from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.services.database import db
from backend.app.agents.super_agent import super_agent

db.ensure_seeded()
questions=[
    "Find the best sales opportunities",
    "Who should I reach out to at RedStone Energy regarding network modernization?",
    "Which support tickets need immediate escalation?",
    "What are our biggest finance variances?",
    "Which inventory items are at risk of stockout?",
    "Give me an executive brief across the business",
    "What is our travel reimbursement policy?",
]
for q in questions:
    r=super_agent.ask(q)
    print("\nQUESTION:",q)
    print("AGENT:",r.agent,"| INTENT:",r.intent)
    print("ANSWER:",r.answer)
    for action in r.recommended_actions:
        print(" -",action)
