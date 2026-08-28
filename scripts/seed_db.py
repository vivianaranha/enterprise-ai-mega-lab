from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.services.database import db

if __name__ == "__main__":
    db.seed(force=True)
    print(f"Seeded enterprise database at: {db.path}")
