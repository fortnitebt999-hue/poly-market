"""Append-only trade log (data/trades.csv)."""
import csv
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRADES_FILE = DATA_DIR / "trades.csv"

FIELDS = ["time", "action", "market_id", "question", "outcome",
          "price", "shares", "amount", "profit"]


def log(action, market_id, question, outcome, price, shares, amount, profit=""):
    DATA_DIR.mkdir(exist_ok=True)
    new = not TRADES_FILE.exists()
    with TRADES_FILE.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "action": action,
            "market_id": market_id,
            "question": question[:80],
            "outcome": outcome,
            "price": price,
            "shares": shares,
            "amount": round(amount, 2),
            "profit": profit,
        })
