"""Inline keyboards for the main bot menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import (
    CALLBACK_ASK_AI,
    CALLBACK_HELP,
    CALLBACK_MARKET,
    CALLBACK_PRICES,
    CALLBACK_SEARCH_COIN,
    CALLBACK_MAIN_MENU,
)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📈 Coin Prices", callback_data=CALLBACK_PRICES),
                InlineKeyboardButton("🔎 Search Coin", callback_data=CALLBACK_SEARCH_COIN),
            ],
            [
                InlineKeyboardButton("📊 Market Dashboard", callback_data=CALLBACK_MARKET),
                InlineKeyboardButton("🤖 Ask AI", callback_data=CALLBACK_ASK_AI),
            ],
            [InlineKeyboardButton("ℹ️ Help", callback_data=CALLBACK_HELP)],
        ]
    )


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data=CALLBACK_MAIN_MENU)]]
    )
