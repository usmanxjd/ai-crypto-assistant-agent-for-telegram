"""Telegram application bootstrap."""

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from bot.config import load_settings
from bot.constants import (
    CALLBACK_ASK_AI,
    CALLBACK_HELP,
    CALLBACK_MARKET,
    CALLBACK_PRICES,
    CALLBACK_PREFIX_EXPLAIN,
    CALLBACK_PREFIX_PRICE,
    CALLBACK_MAIN_MENU,
)
from bot.handlers.ai_chat import answer_ai_question, prompt_for_ai_question
from bot.handlers.prices import explain_coin, show_coin_price, show_market, show_prices
from bot.handlers.start import show_help, show_main_menu, start
from bot.services.coingecko_service import CoinGeckoService
from bot.services.groq_service import GroqService


def build_application() -> Application:
    settings = load_settings()
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.bot_data["settings"] = settings
    application.bot_data["coingecko"] = CoinGeckoService(
        base_url=settings.coingecko_base_url,
        currency=settings.default_currency,
    )
    application.bot_data["groq"] = GroqService(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", show_help))

    application.add_handler(CallbackQueryHandler(show_main_menu, pattern=f"^{CALLBACK_MAIN_MENU}$"))
    application.add_handler(CallbackQueryHandler(show_prices, pattern=f"^{CALLBACK_PRICES}$"))
    application.add_handler(CallbackQueryHandler(show_market, pattern=f"^{CALLBACK_MARKET}$"))
    application.add_handler(CallbackQueryHandler(prompt_for_ai_question, pattern=f"^{CALLBACK_ASK_AI}$"))
    application.add_handler(CallbackQueryHandler(show_help, pattern=f"^{CALLBACK_HELP}$"))
    application.add_handler(CallbackQueryHandler(show_coin_price, pattern=f"^{CALLBACK_PREFIX_PRICE}.+"))
    application.add_handler(CallbackQueryHandler(explain_coin, pattern=f"^{CALLBACK_PREFIX_EXPLAIN}.+"))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_ai_question))

    return application


def run_bot() -> None:
    application = build_application()
    application.run_polling(allowed_updates=["message", "callback_query"])
