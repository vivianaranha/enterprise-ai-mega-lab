from collections import defaultdict
from backend.app.services.database import db

class EnterpriseTools:
    """Read-only enterprise tool layer used by agents.

    Replace these methods with Salesforce, ServiceNow, Workday, SAP, Outlook,
    Teams, MCP servers, or other enterprise connectors as the lab evolves.
    """

    def accounts(self): return db.all("accounts")
    def contacts(self): return db.all("contacts")
    def opportunities(self): return db.all("opportunities")
    def tickets(self): return db.all("tickets")
    def employees(self): return db.all("employees")
    def finance(self): return db.all("finance")
    def inventory(self): return db.all("inventory")
    def shipments(self): return db.all("shipments")
    def meetings(self): return db.all("meetings")

    def account_by_name(self, name: str):
        q = name.lower()
        return next((a for a in self.accounts() if q in a["name"].lower()), None)

    def account_context(self, account_id: str):
        account = db.get("accounts", account_id)
        if not account: return None
        return {
            "account": account,
            "contacts": db.filter("contacts", account_id=account_id),
            "opportunities": db.filter("opportunities", account_id=account_id),
            "tickets": db.filter("tickets", account_id=account_id),
            "meetings": db.filter("meetings", account_id=account_id),
        }

    def sales_opportunity_scores(self):
        accounts = {a["account_id"]: a for a in self.accounts()}
        rows = []
        for opp in self.opportunities():
            acct = accounts[opp["account_id"]]
            score = float(opp["probability"])
            if acct["strategic_tier"] == "Tier 1": score += 10
            if acct["growth_signal"] and acct["growth_signal"] != "None": score += 10
            if acct["health"] == "At Risk": score -= 15
            if float(opp["days_in_stage"]) > 30: score -= 10
            rows.append({**opp, "account_name": acct["name"], "account_health": acct["health"], "growth_signal": acct["growth_signal"], "priority_score": round(score, 1)})
        return sorted(rows, key=lambda x: x["priority_score"], reverse=True)

    def support_escalations(self):
        accounts = {a["account_id"]: a for a in self.accounts()}
        out = []
        for t in self.tickets():
            if t["status"] != "Open": continue
            breach = float(t["age_hours"]) > float(t["sla_hours"])
            critical = t["severity"] == "Critical"
            negative = t["sentiment"] in {"Negative", "Frustrated"}
            if critical or breach or negative:
                out.append({**t, "account_name":accounts[t["account_id"]]["name"], "sla_breached":breach, "strategic_tier":accounts[t["account_id"]]["strategic_tier"]})
        return out

    def finance_variances(self):
        rows=[]
        for r in self.finance():
            budget=float(r["budget_k"]); actual=float(r["actual_k"]); var=float(r["variance_k"])
            pct=(var/budget*100) if budget else 0
            rows.append({**r,"variance_pct":round(pct,1),"needs_review": var>25 or pct>5})
        return sorted(rows,key=lambda x: x["variance_k"],reverse=True)

    def inventory_risks(self):
        rows=[]
        for r in self.inventory():
            weeks=float(r["on_hand"])/max(float(r["weekly_demand"]),1)
            below=float(r["on_hand"]) < float(r["reorder_point"])
            elevated=below and weeks < 2 and float(r["lead_time_days"])>14
            rows.append({**r,"weeks_of_supply":round(weeks,1),"below_reorder_point":below,"risk":"High" if elevated else "Medium" if below else "Low"})
        return sorted(rows,key=lambda x: {"High":0,"Medium":1,"Low":2}[x["risk"]])

tools = EnterpriseTools()
