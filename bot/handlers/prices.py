"""Price, search, and market Telegram handlers."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import (
    CALLBACK_PREFIX_EXPLAIN,
    CALLBACK_PREFIX_PRICE,
    CALLBACK_PREFIX_SEARCH_RESULT,
)
from bot.keyboards.main_menu import back_to_main_keyboard
from bot.keyboards.price_menu import (
    market_actions_keyboard,
    price_actions_keyboard,
    price_menu_keyboard,
    search_results_keyboard,
)
from bot.services.coingecko_service import CoinGeckoService
from bot.services.formatter_service import (
    format_coin_price,
    format_market_dashboard,
    format_search_results,
)
from bot.services.groq_service import GroqService

logger = logging.getLogger(__name__)
FRIENDLY_DATA_ERROR = (
    "I could not load fresh market data right now. The free market data API may be busy. "
    "Please try again in a few seconds."
)


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
        "📈 *Choose a popular coin or search any coin:*",
        parse_mode="Markdown",
        reply_markup=price_menu_keyboard(),
    )


async def prompt_coin_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    context.user_data["awaiting_coin_search"] = True
    context.user_data["awaiting_ai_question"] = False
    await query.edit_message_text(
        "🔎 *Search Coin*\n\nType a coin name or symbol.\n\nExamples: `btc`, `ethereum`, `solana`, `pepe`, `chainlink`.",
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard(),
    )


async def handle_coin_search_text(update: Update, context: ContextTypes.DEFAULT_TYPE, query_text: str) -> None:
    message = update.effective_message
    if not message:
        return

    service = get_coingecko(context)
    try:
        results = await service.search_coins(query_text)
        text = format_search_results(query_text, results)
        keyboard = search_results_keyboard(results) if results else back_to_main_keyboard()
        await message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    except Exception:
        logger.exception("Failed to search coin: %s", query_text)
        await message.reply_text(FRIENDLY_DATA_ERROR, reply_markup=back_to_main_keyboard())


async def show_coin_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    coin_id = query.data.replace(CALLBACK_PREFIX_PRICE, "", 1).replace(
        CALLBACK_PREFIX_SEARCH_RESULT, "", 1
    )
    service = get_coingecko(context)

    try:
        data = await service.get_coin_market_data(coin_id)
        text = format_coin_price(data, service.currency)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=price_actions_keyboard(coin_id),
        )
    except Exception:
        logger.exception("Failed to fetch coin price: %s", coin_id)
        await query.edit_message_text(FRIENDLY_DATA_ERROR, reply_markup=price_menu_keyboard())


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
    except Exception:
        logger.exception("Failed to explain coin: %s", coin_id)
        await query.edit_message_text(
            "I could not create an AI explanation right now. Please try again in a moment.",
            reply_markup=price_actions_keyboard(coin_id),
        )


async def build_market_dashboard_text(context: ContextTypes.DEFAULT_TYPE) -> str:
    service = get_coingecko(context)
    popular = await service.get_popular_market_data()
    global_data = await service.get_global_market_data()
    movers = await service.get_top_movers()
    trending = await service.get_trending_coins()
    return format_market_dashboard(popular, global_data, movers, trending, service.currency)


async def show_market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()

    try:
        text = await build_market_dashboard_text(context)
        context.user_data["last_market_dashboard"] = text
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=market_actions_keyboard())
    except Exception:
        logger.exception("Failed to fetch market dashboard")
        await query.edit_message_text(FRIENDLY_DATA_ERROR, reply_markup=back_to_main_keyboard())


async def show_ai_market_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer("Creating AI market summary...")

    try:
        dashboard = context.user_data.get("last_market_dashboard") or await build_market_dashboard_text(context)
        summary = await get_groq(context).summarize_market(dashboard)
        await query.edit_message_text(summary, parse_mode="Markdown", reply_markup=market_actions_keyboard())
    except Exception:
        logger.exception("Failed to create AI market summary")
        await query.edit_message_text(
            "I could not create the AI market summary right now. Please try again in a moment.",
            reply_markup=market_actions_keyboard(),
        )
