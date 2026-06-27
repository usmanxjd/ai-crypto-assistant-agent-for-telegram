"""AI chat and natural text handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.prices import handle_coin_search_text
from bot.keyboards.main_menu import back_to_main_keyboard
from bot.services.groq_service import GroqService

ASK_AI_PROMPT = (
    "🤖 *Ask AI*\n\n"
    "Send me a crypto question in normal language.\n\n"
    "Examples:\n"
    "• What is Bitcoin?\n"
    "• Explain Ethereum gas fees.\n"
    "• What does market cap mean?\n"
    "• Why is crypto volatile?"
)

PRICE_KEYWORDS = ("price", "chart", "coin", "token", "search")


def get_groq(context: ContextTypes.DEFAULT_TYPE) -> GroqService:
    return context.application.bot_data["groq"]


async def prompt_for_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    context.user_data["awaiting_ai_question"] = True
    context.user_data["awaiting_coin_search"] = False
    await query.edit_message_text(ASK_AI_PROMPT, parse_mode="Markdown", reply_markup=back_to_main_keyboard())


def looks_like_coin_search(text: str) -> str | None:
    normalized = text.strip().lower()
    if not normalized:
        return None

    words = normalized.split()
    if words[0] in {"search", "find"} and len(words) > 1:
        return " ".join(words[1:])
    if len(words) <= 3 and any(keyword in words for keyword in PRICE_KEYWORDS):
        return " ".join(word for word in words if word not in PRICE_KEYWORDS)
    if len(words) == 1 and len(words[0]) <= 12:
        return words[0]
    return None


async def answer_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    text = message.text.strip()

    if context.user_data.get("awaiting_coin_search"):
        context.user_data["awaiting_coin_search"] = False
        await handle_coin_search_text(update, context, text)
        return

    coin_query = looks_like_coin_search(text)
    if coin_query and not context.user_data.get("awaiting_ai_question"):
        await handle_coin_search_text(update, context, coin_query)
        return

    context.user_data["awaiting_ai_question"] = False
    await message.chat.send_action("typing")
    answer = await get_groq(context).answer_crypto_question(text)
    await message.reply_text(answer, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
