"""Price and market Telegram handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import CALLBACK_PREFIX_EXPLAIN, CALLBACK_PREFIX_PRICE
from bot.keyboards.main_menu import back_to_main_keyboard
from bot.keyboards.price_menu import price_actions_keyboard, price_menu_keyboard
from bot.services.coingecko_service import CoinGeckoService
from bot.services.formatter_service import format_coin_price, format_market_summary
from bot.services.groq_service import GroqService


def get_coingecko(context: ContextTypes.DEFAULT_TYPE) -> CoinGeckoService:
    return context.application.bot_data["coingecko"]


def get_groq(context: ContextTypes.DEFAULT_TYPE) -> GroqService:
    return context.application.bot_data["groq"]


async def show_prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    await query.edit_message_text(
        "📈 *Choose a coin:*", parse_mode="Markdown", reply_markup=price_menu_keyboard()
    )


async def show_coin_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    coin_id = query.data.replace(CALLBACK_PREFIX_PRICE, "", 1)
    service = get_coingecko(context)

    try:
        data = await service.get_coin_market_data(coin_id)
        text = format_coin_price(data, service.currency)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=price_actions_keyboard(coin_id),
        )
    except Exception as exc:  # noqa: BLE001 - user-facing fallback for external API errors
        await query.edit_message_text(
            f"⚠️ Could not fetch price right now. Please try again later.\n\nError: {exc}",
            reply_markup=price_menu_keyboard(),
        )


async def explain_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer("Creating AI explanation...")
    coin_id = query.data.replace(CALLBACK_PREFIX_EXPLAIN, "", 1)

    try:
        coin_data = await get_coingecko(context).get_coin_market_data(coin_id)
        text = await get_groq(context).explain_coin(coin_data)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=price_actions_keyboard(coin_id))
    except Exception as exc:  # noqa: BLE001 - user-facing fallback for external API errors
        await query.edit_message_text(
            f"⚠️ Could not create explanation right now. Please try again later.\n\nError: {exc}",
            reply_markup=price_actions_keyboard(coin_id),
        )


async def show_market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()

    try:
        service = get_coingecko(context)
        data = await service.get_popular_market_data()
        text = format_market_summary(data, service.currency)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    except Exception as exc:  # noqa: BLE001 - user-facing fallback for external API errors
        await query.edit_message_text(
            f"⚠️ Could not fetch market data right now. Please try again later.\n\nError: {exc}",
            reply_markup=back_to_main_keyboard(),
        )
