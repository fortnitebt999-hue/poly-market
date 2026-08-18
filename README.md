# Poly Market Paper Bot

Automated Polymarket trading bot — **paper mode**. Reads real live Polymarket
prices, makes real decisions, spends **fake money** from a simulated wallet
with hard spending limits. Goal: prove (or disprove) the strategy is
profitable before any real money is involved.

## Rules

- **No real money in this repo.** No wallet keys, no API credentials, ever.
- All spending limits live in `bot/config.py` and are enforced by
  `bot/paper_wallet.py` — the bot physically cannot exceed them.
- `data/` (your wallet + trade history) is gitignored — each person runs
  their own simulation.

## Setup

```
git clone https://github.com/fortnitebt999-hue/poly-market.git
cd poly-market
pip install -r requirements.txt
```

## Run one cycle

```
python -m bot.run
```

Each run: settles any resolved markets, scans the top-volume open markets,
buys what the strategy picks (fake money), prints P&L. Run it once a day
(or hourly) for a couple of weeks — the P&L line answers "does this
strategy make money?"

Reset your simulation: delete the `data/` folder.

## How it works

| File | Job |
|------|-----|
| `bot/config.py` | Spending limits + strategy knobs (edit freely) |
| `bot/market_data.py` | Live prices from Polymarket's public Gamma API |
| `bot/strategy.py` | Decides what to buy (v1: heavy favorites 90-97¢) |
| `bot/paper_wallet.py` | Fake wallet, enforces the caps |
| `bot/ledger.py` | Logs every trade to `data/trades.csv` |
| `bot/run.py` | Glues one cycle together |

## Workflow

1. `git pull` before starting
2. Work on a branch: `git checkout -b your-feature`
3. Push and open a Pull Request
