"""Read-only Polymarket data via the public Gamma API. No auth, no real trading."""
import json

import requests

GAMMA = "https://gamma-api.polymarket.com"


def _parse(raw):
    try:
        outcomes = json.loads(raw["outcomes"])
        prices = [float(p) for p in json.loads(raw["outcomePrices"])]
    except (KeyError, ValueError, TypeError):
        return None
    if len(outcomes) != len(prices):
        return None
    return {
        "id": str(raw["id"]),
        "question": raw.get("question", ""),
        "slug": raw.get("slug", ""),
        "outcomes": outcomes,
        "prices": prices,
        "volume_24h": float(raw.get("volume24hr") or raw.get("volume") or 0),
        "end_date": raw.get("endDate", ""),
        "closed": raw.get("closed", False),
    }


def open_markets(limit=100):
    r = requests.get(f"{GAMMA}/markets", params={
        "closed": "false",
        "active": "true",
        "limit": limit,
        "order": "volume24hr",
        "ascending": "false",
    }, timeout=30)
    r.raise_for_status()
    markets = [_parse(m) for m in r.json()]
    return [m for m in markets if m]


def market_by_id(market_id):
    r = requests.get(f"{GAMMA}/markets/{market_id}", timeout=30)
    r.raise_for_status()
    return _parse(r.json())
