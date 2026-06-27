"""Telegram-friendly message formatters."""

from __future__ import annotations

from bot.constants import DISCLAIMER


def money(value: float | int | None, currency: str = "usd") -> str:
    if value is None:
        return "N/A"
    symbol = "$" if currency.lower() == "usd" else f"{currency.upper()} "
    if value >= 1:
        return f"{symbol}{value:,.2f}"
    return f"{symbol}{value:,.8f}"


def percentage(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def format_coin_price(data: dict, currency: str = "usd") -> str:
    name = data.get("name", "Unknown")
    symbol = data.get("symbol", "").upper()
    price = money(data.get("current_price"), currency)
    change_24h = percentage(data.get("price_change_percentage_24h"))
    market_cap = money(data.get("market_cap"), currency)
    volume = money(data.get("total_volume"), currency)

    return (
        f"📈 *{name} ({symbol})*\n\n"
        f"Price: *{price}*\n"
        f"24h Change: *{change_24h}*\n"
        f"Market Cap: {market_cap}\n"
        f"24h Volume: {volume}\n\n"
        "Data source: CoinGecko"
    )


def format_market_summary(coins: list[dict], currency: str = "usd") -> str:
    lines = ["📊 *Crypto Market Snapshot*", ""]
    positive = 0
    negative = 0

    for coin in coins:
        symbol = coin.get("symbol", "").upper()
        price = money(coin.get("current_price"), currency)
        change = coin.get("price_change_percentage_24h")
        if change is not None and change >= 0:
            positive += 1
        elif change is not None:
            negative += 1
        lines.append(f"*{symbol}*: {price} ({percentage(change)})")

    if positive > negative:
        mood = "Most tracked coins are positive today."
    elif negative > positive:
        mood = "Most tracked coins are negative today."
    else:
        mood = "The tracked market looks mixed today."

    lines.extend(["", f"Quick read: {mood}", "", DISCLAIMER])
    return "\n".join(lines)
