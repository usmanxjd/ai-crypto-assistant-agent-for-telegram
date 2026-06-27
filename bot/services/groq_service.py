"""Groq Cloud AI helper service."""

from __future__ import annotations

from groq import AsyncGroq

from bot.constants import DISCLAIMER


class GroqService:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self.client = AsyncGroq(api_key=api_key) if api_key else None

    async def answer_crypto_question(self, question: str) -> str:
        if not self.client:
            return (
                "🤖 AI is not configured yet. Add `GROQ_API_KEY` to your `.env` file, "
                "then restart the bot."
            )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly crypto education assistant inside a Telegram bot. "
                        "Reply in clear beginner-friendly language. Keep answers concise but useful. "
                        "Do not guarantee profits. Do not provide private-key, seed-phrase, pump-and-dump, "
                        "or scam instructions. If the user asks whether to buy or sell, explain pros/cons "
                        "and include a natural risk note instead of giving direct financial advice."
                    ),
                },
                {"role": "user", "content": question},
            ],
            temperature=0.4,
            max_tokens=650,
        )
        answer = response.choices[0].message.content or "I could not generate an answer."
        return f"🤖 *AI Crypto Assistant*\n\n{answer}"

    async def explain_coin(self, coin_data: dict) -> str:
        name = coin_data.get("name", "this coin")
        symbol = coin_data.get("symbol", "").upper()
        prompt = (
            f"Explain today's basic market data for {name} ({symbol}) in simple beginner language. "
            f"Price: {coin_data.get('current_price')}. "
            f"24h change: {coin_data.get('price_change_percentage_24h')}. "
            f"7d change: {coin_data.get('price_change_percentage_7d_in_currency')}. "
            f"Market cap: {coin_data.get('market_cap')}. "
            f"24h volume: {coin_data.get('total_volume')}. "
            "Do not tell the user to buy or sell."
        )
        return await self.answer_crypto_question(prompt)

    async def summarize_market(self, dashboard_text: str) -> str:
        prompt = (
            "Create a beginner-friendly crypto market summary from this dashboard. "
            "Mention overall market mood, strongest/weakest areas, and what a user should watch next. "
            f"Keep it educational.\n\n{dashboard_text}\n\n{DISCLAIMER}"
        )
        return await self.answer_crypto_question(prompt)
