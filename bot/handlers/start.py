"""Start and help handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import DISCLAIMER
from bot.keyboards.main_menu import back_to_main_keyboard, main_menu_keyboard

WELCOME_TEXT = (
    "👋 *Welcome to Crypto AI Assistant*\n\n"
    "Use the buttons below to explore crypto prices, market snapshots, and AI explanations.\n\n"
    "What would you like to do?"
)

HELP_TEXT = (
    "ℹ️ *How to Use This Bot*\n\n"
    "📈 *Prices* — check live prices for popular coins.\n"
    "📊 *Market* — see a quick snapshot of tracked coins.\n"
    "🤖 *Ask AI* — ask beginner-friendly crypto questions.\n\n"
    "Coming next: watchlists, price alerts, news summaries, and portfolio tracking.\n\n"
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
