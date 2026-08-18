"""Simulated wallet. Enforces the spending limits — the bot cannot exceed them."""
import json
from pathlib import Path

from bot import config

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
WALLET_FILE = DATA_DIR / "wallet.json"


class LimitExceeded(Exception):
    pass


def load():
    if WALLET_FILE.exists():
        return json.loads(WALLET_FILE.read_text())
    return {"cash": config.STARTING_CASH, "positions": {}}


def save(wallet):
    DATA_DIR.mkdir(exist_ok=True)
    WALLET_FILE.write_text(json.dumps(wallet, indent=2))


def exposure(wallet):
    return sum(p["cost"] for p in wallet["positions"].values())


def buy(wallet, market_id, question, outcome, outcome_index, price, amount):
    if amount > config.MAX_PER_TRADE:
        raise LimitExceeded(f"${amount:.2f} > per-trade cap ${config.MAX_PER_TRADE:.2f}")
    if amount > wallet["cash"]:
        raise LimitExceeded("not enough cash")
    if exposure(wallet) + amount > config.MAX_TOTAL_EXPOSURE:
        raise LimitExceeded("total exposure cap reached")
    key = f"{market_id}:{outcome_index}"
    if key in wallet["positions"]:
        raise LimitExceeded("already holding this market")
    shares = round(amount / price, 4)
    wallet["cash"] -= amount
    wallet["positions"][key] = {
        "market_id": market_id,
        "question": question,
        "outcome": outcome,
        "outcome_index": outcome_index,
        "entry_price": price,
        "shares": shares,
        "cost": amount,
    }
    return wallet["positions"][key]


def settle(wallet, key, final_price):
    pos = wallet["positions"].pop(key)
    payout = round(pos["shares"] * final_price, 2)
    wallet["cash"] += payout
    profit = payout - pos["cost"]
    return pos, payout, profit
