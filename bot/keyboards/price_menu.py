"""Inline keyboards for price-related actions."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import (
    CALLBACK_MARKET_AI,
    CALLBACK_PREFIX_EXPLAIN,
    CALLBACK_PREFIX_PRICE,
    CALLBACK_PREFIX_SEARCH_RESULT,
    CALLBACK_SEARCH_COIN,
    CALLBACK_MAIN_MENU,
    POPULAR_COINS,
)


def price_menu_keyboard() -> InlineKeyboardMarkup:
    rows = []
    coin_items = list(POPULAR_COINS.items())
    for index in range(0, len(coin_items), 2):
        row = []
        for coin_id, coin in coin_items[index : index + 2]:
            row.append(
                InlineKeyboardButton(
                    coin["symbol"], callback_data=f"{CALLBACK_PREFIX_PRICE}{coin_id}"
                )
            )
        rows.append(row)

    rows.append([InlineKeyboardButton("🔎 Search Any Coin", callback_data=CALLBACK_SEARCH_COIN)])
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data=CALLBACK_MAIN_MENU)])
    return InlineKeyboardMarkup(rows)


def search_results_keyboard(results: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for result in results[:8]:
        name = result.get("name", "Unknown")
        symbol = result.get("symbol", "").upper()
        coin_id = result.get("id")
        if not coin_id:
            continue
        rows.append(
            [
                InlineKeyboardButton(
                    f"{name} ({symbol})",
                    callback_data=f"{CALLBACK_PREFIX_SEARCH_RESULT}{coin_id}",
                )
            ]
        )
    rows.append([InlineKeyboardButton("🔎 Search Again", callback_data=CALLBACK_SEARCH_COIN)])
    rows.append([InlineKeyboardButton("⬅️ Back to Prices", callback_data="prices")])
    return InlineKeyboardMarkup(rows)


def price_actions_keyboard(coin_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data=f"{CALLBACK_PREFIX_PRICE}{coin_id}"),
                InlineKeyboardButton("🤖 Explain", callback_data=f"{CALLBACK_PREFIX_EXPLAIN}{coin_id}"),
            ],
            [
                InlineKeyboardButton("🔎 Search Again", callback_data=CALLBACK_SEARCH_COIN),
                InlineKeyboardButton("⬅️ Back to Prices", callback_data="prices"),
            ],
        ]
    )


def market_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🤖 AI Market Summary", callback_data=CALLBACK_MARKET_AI)],
            [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="market")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data=CALLBACK_MAIN_MENU)],
        ]
    )
