"""One bot cycle: settle -> decide -> paper-buy -> report.

Run repeatedly (e.g. once a day):
    python -m bot.run

Paper mode only — no real money anywhere in this codebase.
"""
from bot import config, ledger, market_data, paper_wallet, strategy


def settle_and_value(wallet):
    """Settle positions whose markets closed; mark open ones to current price."""
    open_value = 0.0
    for key in list(wallet["positions"].keys()):
        pos = wallet["positions"][key]
        try:
            m = market_data.market_by_id(pos["market_id"])
        except Exception as e:
            print(f"  ! could not fetch market {pos['market_id']}: {e}")
            open_value += pos["cost"]
            continue
        if m is None:
            open_value += pos["cost"]
            continue
        price = m["prices"][pos["outcome_index"]]
        if m["closed"]:
            pos, payout, profit = paper_wallet.settle(wallet, key, price)
            ledger.log("SETTLE", pos["market_id"], pos["question"], pos["outcome"],
                       price, pos["shares"], payout, round(profit, 2))
            tag = "WIN" if profit > 0 else "LOSS"
            print(f"  settled {tag} ${profit:+.2f}: {pos['question'][:60]}")
        else:
            open_value += pos["shares"] * price
    return open_value


def main():
    wallet = paper_wallet.load()
    print("=== poly-market paper bot ===")
    print(f"cash ${wallet['cash']:.2f} | open positions: {len(wallet['positions'])}")

    open_value = settle_and_value(wallet)

    markets = market_data.open_markets()
    print(f"scanned {len(markets)} markets")

    orders = strategy.decide(markets, wallet)
    for o in orders:
        try:
            pos = paper_wallet.buy(wallet, o["market_id"], o["question"], o["outcome"],
                                   o["outcome_index"], o["price"], o["amount"])
        except paper_wallet.LimitExceeded as e:
            print(f"  skip ({e}): {o['question'][:60]}")
            continue
        ledger.log("BUY", o["market_id"], o["question"], o["outcome"],
                   o["price"], pos["shares"], o["amount"])
        open_value += o["amount"]
        print(f"  BUY ${o['amount']:.2f} '{o['outcome']}' @ {o['price']:.2f} | {o['question'][:60]}")
    if not orders:
        print("  no new trades this run")

    paper_wallet.save(wallet)
    total = wallet["cash"] + open_value
    pnl = total - config.STARTING_CASH
    print(f"--- cash ${wallet['cash']:.2f} + open ${open_value:.2f} = ${total:.2f} "
          f"| P&L {pnl:+.2f} vs ${config.STARTING_CASH:.0f} start")


if __name__ == "__main__":
    main()
