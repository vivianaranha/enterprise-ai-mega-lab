import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from backend.app.config import settings

TABLE_FILES = {
    "accounts": "accounts.csv",
    "contacts": "contacts.csv",
    "opportunities": "opportunities.csv",
    "tickets": "tickets.csv",
    "employees": "employees.csv",
    "finance": "finance.csv",
    "inventory": "inventory.csv",
    "shipments": "shipments.csv",
    "meetings": "meetings.csv",
}

PRIMARY_KEYS = {
    "accounts": "account_id",
    "contacts": "contact_id",
    "opportunities": "opportunity_id",
    "tickets": "ticket_id",
    "employees": "employee_id",
    "finance": None,
    "inventory": "sku",
    "shipments": "shipment_id",
    "meetings": "meeting_id",
}

NUMERIC_COLUMNS = {
    "accounts": {"annual_revenue_m", "employees"},
    "opportunities": {"amount_k", "probability", "days_in_stage"},
    "tickets": {"age_hours", "sla_hours"},
    "employees": {"tenure_years"},
    "finance": {"budget_k", "actual_k", "variance_k", "forecast_k"},
    "inventory": {"on_hand", "reorder_point", "weekly_demand", "lead_time_days", "unit_cost"},
    "shipments": {"days_late"},
}

class Database:
    def __init__(self, path: str | None = None):
        self.path = path or settings.database_path

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def seed(self, force: bool = False):
        db_path = Path(self.path)
        if force and db_path.exists():
            db_path.unlink()
        data_dir = settings.project_root / "data"
        with self.connect() as conn:
            for table, filename in TABLE_FILES.items():
                rows = list(csv.DictReader((data_dir / filename).open(encoding="utf-8")))
                if not rows:
                    continue
                for row in rows:
                    for col in NUMERIC_COLUMNS.get(table, set()):
                        if col in row and row[col] != "":
                            row[col] = float(row[col])
                cols = list(rows[0].keys())
                pk = PRIMARY_KEYS.get(table)
                column_sql = []
                for col in cols:
                    typ = "REAL" if col in NUMERIC_COLUMNS.get(table, set()) else "TEXT"
                    extra = " PRIMARY KEY" if pk == col else ""
                    column_sql.append(f'"{col}" {typ}{extra}')
                conn.execute(f'DROP TABLE IF EXISTS "{table}"')
                conn.execute(f'CREATE TABLE "{table}" ({", ".join(column_sql)})')
                placeholders = ",".join(["?"] * len(cols))
                quoted_cols = ",".join([f'"{c}"' for c in cols])
                conn.executemany(
                    f'INSERT INTO "{table}" ({quoted_cols}) VALUES ({placeholders})',
                    [[r[c] for c in cols] for r in rows]
                )
            conn.execute("""CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                user_role TEXT,
                message TEXT,
                selected_agent TEXT,
                intent TEXT,
                metadata_json TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                proposed_change_json TEXT,
                reason TEXT
            )""")
            conn.commit()

    def ensure_seeded(self):
        with self.connect() as conn:
            row = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'").fetchone()
        if not row:
            self.seed()

    def all(self, table: str) -> List[Dict[str, Any]]:
        self._check_table(table)
        with self.connect() as conn:
            return [dict(r) for r in conn.execute(f'SELECT * FROM "{table}"').fetchall()]

    def get(self, table: str, entity_id: str) -> Optional[Dict[str, Any]]:
        self._check_table(table)
        pk = PRIMARY_KEYS.get(table)
        if not pk:
            return None
        with self.connect() as conn:
            row = conn.execute(f'SELECT * FROM "{table}" WHERE "{pk}"=?', (entity_id,)).fetchone()
            return dict(row) if row else None

    def filter(self, table: str, **filters) -> List[Dict[str, Any]]:
        self._check_table(table)
        if not filters:
            return self.all(table)
        clauses, values = [], []
        for key, value in filters.items():
            clauses.append(f'"{key}"=?')
            values.append(value)
        sql = f'SELECT * FROM "{table}" WHERE ' + " AND ".join(clauses)
        with self.connect() as conn:
            return [dict(r) for r in conn.execute(sql, values).fetchall()]

    def search(self, table: str, query: str) -> List[Dict[str, Any]]:
        self._check_table(table)
        rows = self.all(table)
        q = query.lower()
        return [r for r in rows if q in " ".join(str(v).lower() for v in r.values())]

    def insert_audit(self, created_at, user_role, message, selected_agent, intent, metadata):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO audit_log(created_at,user_role,message,selected_agent,intent,metadata_json) VALUES (?,?,?,?,?,?)",
                (created_at,user_role,message,selected_agent,intent,json.dumps(metadata))
            )
            conn.commit()

    def create_approval(self, created_at, action, entity_type, entity_id, proposed_change, reason):
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO approvals(created_at,status,action,entity_type,entity_id,proposed_change_json,reason) VALUES (?,?,?,?,?,?,?)",
                (created_at,"pending",action,entity_type,entity_id,json.dumps(proposed_change),reason)
            )
            conn.commit()
            return cur.lastrowid

    def _check_table(self, table: str):
        if table not in TABLE_FILES:
            raise ValueError(f"Unsupported resource: {table}")

db = Database()
