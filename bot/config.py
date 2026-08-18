"""All limits and strategy knobs in one place. Edit here, not in the code."""

# --- wallet (fake money, paper mode) ---
STARTING_CASH = 1000.00      # simulated USDC
MAX_PER_TRADE = 50.00        # hard cap per single trade
MAX_TOTAL_EXPOSURE = 500.00  # hard cap on total cash deployed at once

# --- strategy: heavy favorites ---
MIN_PRICE = 0.90             # only buy outcomes priced in this band
MAX_PRICE = 0.97
MIN_VOLUME_24H = 10_000      # skip thin markets (24h volume, USD)
MAX_DAYS_TO_END = 7          # only markets resolving within a week
MAX_NEW_TRADES_PER_RUN = 3
