"""Inline keyboards for price-related actions."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import CALLBACK_PREFIX_EXPLAIN, CALLBACK_PREFIX_PRICE, CALLBACK_MAIN_MENU, POPULAR_COINS


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

    rows.append([InlineKeyboardButton("⬅️ Back", callback_data=CALLBACK_MAIN_MENU)])
    return InlineKeyboardMarkup(rows)


def price_actions_keyboard(coin_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data=f"{CALLBACK_PREFIX_PRICE}{coin_id}"),
                InlineKeyboardButton("🤖 Explain", callback_data=f"{CALLBACK_PREFIX_EXPLAIN}{coin_id}"),
            ],
            [InlineKeyboardButton("⬅️ Back to Prices", callback_data="prices")],
        ]
    )
