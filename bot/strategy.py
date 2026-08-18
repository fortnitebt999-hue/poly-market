"""Trading strategy. decide() returns orders; it never touches the wallet directly.

v1 placeholder: "heavy favorite" — buy outcomes priced 0.90-0.97 in
high-volume markets ending within a week. Swap this file to try other ideas.
"""
from datetime import datetime, timezone

from bot import config


def _days_to_end(end_date):
    try:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (end - datetime.now(timezone.utc)).days


def decide(markets, wallet):
    orders = []
    held = set(wallet["positions"].keys())
    for m in markets:
        if len(orders) >= config.MAX_NEW_TRADES_PER_RUN:
            break
        if m["volume_24h"] < config.MIN_VOLUME_24H:
            continue
        days = _days_to_end(m["end_date"])
        if days is None or days < 0 or days > config.MAX_DAYS_TO_END:
            continue
        for i, price in enumerate(m["prices"]):
            key = f"{m['id']}:{i}"
            if key in held:
                continue
            if config.MIN_PRICE <= price <= config.MAX_PRICE:
                orders.append({
                    "market_id": m["id"],
                    "question": m["question"],
                    "outcome": m["outcomes"][i],
                    "outcome_index": i,
                    "price": price,
                    "amount": config.MAX_PER_TRADE,
                })
                break
    return orders
