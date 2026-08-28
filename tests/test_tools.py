from backend.app.services.database import db
from backend.app.services.tools import tools

def setup_module():
    db.seed(force=True)

def test_sales_scores_sorted():
    rows=tools.sales_opportunity_scores()
    assert len(rows)>0
    assert rows[0]["priority_score"] >= rows[-1]["priority_score"]

def test_support_escalations_exist():
    rows=tools.support_escalations()
    assert any(r["severity"]=="Critical" for r in rows)

def test_inventory_risk():
    rows=tools.inventory_risks()
    assert any(r["risk"] in {"High","Medium"} for r in rows)
