"""Start and help handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import DISCLAIMER
from bot.keyboards.main_menu import back_to_main_keyboard, main_menu_keyboard

WELCOME_TEXT = (
    "👋 *Welcome to Crypto AI Assistant*\n\n"
    "Check coin prices, search any crypto, view a market dashboard, or ask AI questions in normal language.\n\n"
    "You can use the buttons below, or simply type things like:\n"
    "• `btc price`\n"
    "• `search pepe`\n"
    "• `what is market cap?`\n\n"
    "What would you like to do?"
)

HELP_TEXT = (
    "ℹ️ *How to Use This Bot*\n\n"
    "📈 *Coin Prices* — check popular coin price cards.\n"
    "🔎 *Search Coin* — search any coin by name or symbol.\n"
    "📊 *Market Dashboard* — view global stats, movers, and trending coins.\n"
    "🤖 *Ask AI* — ask beginner-friendly crypto questions.\n\n"
    "You can also type naturally, for example `bitcoin price` or `explain ethereum gas fees`.\n\n"
    f"_{DISCLAIMER}_"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message:
        await message.reply_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_menu_keyboard())


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(HELP_TEXT, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
        return

    message = update.effective_message
    if message:
        await message.reply_text(HELP_TEXT, parse_mode="Markdown", reply_markup=back_to_main_keyboard())


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_menu_keyboard())
