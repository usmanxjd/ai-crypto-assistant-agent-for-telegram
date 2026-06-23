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
                "🤖 AI is not configured yet. Add GROQ_API_KEY to your .env file, "
                "then restart the bot."
            )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly crypto education assistant inside a Telegram bot. "
                        "Explain concepts simply. Do not guarantee profits. Do not provide private-key, "
                        "seed-phrase, pump-and-dump, or scam instructions. Always include a short risk note."
                    ),
                },
                {"role": "user", "content": question},
            ],
            temperature=0.4,
            max_tokens=600,
        )
        answer = response.choices[0].message.content or "I could not generate an answer."
        return f"🤖 *AI Crypto Assistant*\n\n{answer}\n\n_{DISCLAIMER}_"

    async def explain_coin(self, coin_data: dict) -> str:
        name = coin_data.get("name", "this coin")
        symbol = coin_data.get("symbol", "").upper()
        prompt = (
            f"Explain today's basic market data for {name} ({symbol}) in simple beginner language. "
            f"Price: {coin_data.get('current_price')}. "
            f"24h change: {coin_data.get('price_change_percentage_24h')}. "
            f"Market cap: {coin_data.get('market_cap')}. "
            f"24h volume: {coin_data.get('total_volume')}. "
            "Do not tell the user to buy or sell."
        )
        return await self.answer_crypto_question(prompt)
