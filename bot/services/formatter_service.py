"""Telegram-friendly message formatters."""

from __future__ import annotations

from statistics import mean

from bot.constants import DISCLAIMER


def money(value: float | int | None, currency: str = "usd") -> str:
    if value is None:
        return "N/A"
    symbol = "$" if currency.lower() == "usd" else f"{currency.upper()} "
    if abs(value) >= 1_000_000_000_000:
        return f"{symbol}{value / 1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000:
        return f"{symbol}{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{symbol}{value / 1_000_000:.2f}M"
    if abs(value) >= 1:
        return f"{symbol}{value:,.2f}"
    return f"{symbol}{value:,.8f}"


def compact_number(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:,.2f}"


def percentage(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def format_coin_price(data: dict, currency: str = "usd") -> str:
    name = data.get("name", "Unknown")
    symbol = data.get("symbol", "").upper()
    price = money(data.get("current_price"), currency)
    change_24h = data.get("price_change_percentage_24h")
    change_7d = data.get("price_change_percentage_7d_in_currency")
    market_cap = money(data.get("market_cap"), currency)
    volume = money(data.get("total_volume"), currency)
    high_24h = money(data.get("high_24h"), currency)
    low_24h = money(data.get("low_24h"), currency)
    rank = data.get("market_cap_rank") or "N/A"
    supply = compact_number(data.get("circulating_supply"))

    if change_24h is None:
        quick_read = "Not enough 24h data is available for a quick read."
    elif change_24h > 3:
        quick_read = "Strong positive 24h move. Momentum is active, but volatility can reverse quickly."
    elif change_24h > 0:
        quick_read = "Slightly positive 24h move. Buyers have a small short-term edge."
    elif change_24h > -3:
        quick_read = "Slightly negative 24h move. The coin is cooling off but not sharply."
    else:
        quick_read = "Sharp negative 24h move. Risk and volatility are elevated."

    return (
        f"📈 *{name} ({symbol})*\n\n"
        f"💵 Price: *{price}*\n"
        f"📊 24h Change: *{percentage(change_24h)}*\n"
        f"📅 7d Change: {percentage(change_7d)}\n"
        f"📈 24h High: {high_24h}\n"
        f"📉 24h Low: {low_24h}\n"
        f"🏦 Market Cap: {market_cap}\n"
        f"🔁 24h Volume: {volume}\n"
        f"🏆 Market Rank: #{rank}\n"
        f"📦 Circulating Supply: {supply} {symbol}\n\n"
        f"🧠 Quick read: {quick_read}\n\n"
        "Data source: CoinGecko"
    )


def format_market_dashboard(
    popular_coins: list[dict],
    global_data: dict,
    movers: dict[str, list[dict]],
    trending: list[dict],
    currency: str = "usd",
) -> str:
    market_cap = global_data.get("total_market_cap", {}).get(currency)
    volume = global_data.get("total_volume", {}).get(currency)
    market_change = global_data.get("market_cap_change_percentage_24h_usd")
    btc_dominance = global_data.get("market_cap_percentage", {}).get("btc")
    eth_dominance = global_data.get("market_cap_percentage", {}).get("eth")

    changes = [
        coin.get("price_change_percentage_24h")
        for coin in popular_coins
        if coin.get("price_change_percentage_24h") is not None
    ]
    avg_change = mean(changes) if changes else None
    best = max(popular_coins, key=lambda coin: coin.get("price_change_percentage_24h") or -999)
    weakest = min(popular_coins, key=lambda coin: coin.get("price_change_percentage_24h") or 999)

    lines = [
        "📊 *Crypto Market Dashboard*",
        "",
        "🌍 *Global Market*",
        f"Total Market Cap: {money(market_cap, currency)}",
        f"24h Volume: {money(volume, currency)}",
        f"Market Cap 24h: {percentage(market_change)}",
        f"BTC Dominance: {percentage(btc_dominance)}",
        f"ETH Dominance: {percentage(eth_dominance)}",
        "",
        "⭐ *Tracked Coins*",
    ]

    for coin in popular_coins:
        symbol = coin.get("symbol", "").upper()
        price = money(coin.get("current_price"), currency)
        change = percentage(coin.get("price_change_percentage_24h"))
        lines.append(f"• {symbol}: {price} ({change})")

    lines.extend(
        [
            "",
            "🧭 *Quick Market Read*",
            f"Average tracked 24h move: {percentage(avg_change)}",
            f"Best tracked coin: {best.get('symbol', '').upper()} ({percentage(best.get('price_change_percentage_24h'))})",
            f"Weakest tracked coin: {weakest.get('symbol', '').upper()} ({percentage(weakest.get('price_change_percentage_24h'))})",
            "",
            "🚀 *Top Gainers from Top Market-Cap Coins*",
        ]
    )

    for coin in movers.get("gainers", [])[:3]:
        lines.append(
            f"• {coin.get('symbol', '').upper()}: {percentage(coin.get('price_change_percentage_24h'))}"
        )

    lines.append("")
    lines.append("🔻 *Top Losers from Top Market-Cap Coins*")
    for coin in movers.get("losers", [])[:3]:
        lines.append(
            f"• {coin.get('symbol', '').upper()}: {percentage(coin.get('price_change_percentage_24h'))}"
        )

    lines.append("")
    lines.append("🔥 *Trending Searches*")
    for item in trending[:5]:
        name = item.get("name", "Unknown")
        symbol = item.get("symbol", "").upper()
        lines.append(f"• {name} ({symbol})")

    return "\n".join(lines)


def format_search_results(query: str, results: list[dict]) -> str:
    if not results:
        return (
            f"🔎 I could not find a coin for *{query}*.\n\n"
            "Try another symbol or coin name, for example: `btc`, `ethereum`, `solana`, `pepe`."
        )

    return (
        f"🔎 Search results for *{query}*\n\n"
        "Choose the coin you want from the buttons below."
    )
