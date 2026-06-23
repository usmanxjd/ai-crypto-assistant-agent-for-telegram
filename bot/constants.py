"""Shared constants for the Telegram crypto assistant."""

DISCLAIMER = (
    "This bot provides educational and informational content only. "
    "It is not financial advice. Crypto markets are risky and volatile."
)

POPULAR_COINS = {
    "bitcoin": {"symbol": "BTC", "name": "Bitcoin"},
    "ethereum": {"symbol": "ETH", "name": "Ethereum"},
    "solana": {"symbol": "SOL", "name": "Solana"},
    "binancecoin": {"symbol": "BNB", "name": "BNB"},
    "ripple": {"symbol": "XRP", "name": "XRP"},
    "dogecoin": {"symbol": "DOGE", "name": "Dogecoin"},
}

CALLBACK_MAIN_MENU = "main_menu"
CALLBACK_PRICES = "prices"
CALLBACK_MARKET = "market"
CALLBACK_ASK_AI = "ask_ai"
CALLBACK_HELP = "help"
CALLBACK_BACK = "back"
CALLBACK_PREFIX_PRICE = "price:"
CALLBACK_PREFIX_EXPLAIN = "explain:"
