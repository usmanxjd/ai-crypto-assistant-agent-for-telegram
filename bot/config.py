"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    groq_api_key: str
    groq_model: str
    coingecko_base_url: str
    default_currency: str


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required. Add it to your .env file.")

    return Settings(
        telegram_bot_token=token,
        groq_api_key=os.getenv("GROQ_API_KEY", "").strip(),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip(),
        coingecko_base_url=os.getenv(
            "COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3"
        ).rstrip("/"),
        default_currency=os.getenv("DEFAULT_CURRENCY", "usd").strip().lower(),
    )
