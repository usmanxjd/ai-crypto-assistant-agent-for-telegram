"""AI chat handlers."""

from telegram import Update
from telegram.ext import ContextTypes

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


def get_groq(context: ContextTypes.DEFAULT_TYPE) -> GroqService:
    return context.application.bot_data["groq"]


async def prompt_for_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    context.user_data["awaiting_ai_question"] = True
    await query.edit_message_text(ASK_AI_PROMPT, parse_mode="Markdown", reply_markup=back_to_main_keyboard())


async def answer_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    if not context.user_data.get("awaiting_ai_question"):
        await message.reply_text(
            "Use /start to open the button menu, then choose a feature.",
            reply_markup=back_to_main_keyboard(),
        )
        return

    context.user_data["awaiting_ai_question"] = False
    await message.chat.send_action("typing")
    answer = await get_groq(context).answer_crypto_question(message.text)
    await message.reply_text(answer, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
