# AI Crypto Assistant Agent for Telegram

A beginner-friendly, button-based Telegram crypto assistant built with Python, free-first APIs, and Groq AI.

## What this bot offers

- Button-based Telegram menus instead of command-heavy flows.
- Natural chat support so users can type crypto questions directly.
- Live crypto price checks using CoinGecko's public API.
- Search for coins by name or symbol.
- Detailed market dashboard with global stats, movers, and trending coins.
- AI crypto question answering and market summaries using Groq Cloud.
- Friendly help and financial-risk disclaimer screens.
- A clean architecture that can grow into Fiverr Basic, Standard, and Premium packages.

## MVP workflow

1. User opens the bot and taps `/start`.
2. Bot shows a button menu: Coin Prices, Search Coin, Market Dashboard, Ask AI, Help.
3. User taps a feature button or types naturally.
4. The bot calls the needed service:
   - CoinGecko for live crypto market data, search, global stats, movers, and trending coins.
   - Groq for AI explanations, market summaries, and crypto education.
5. The bot formats the result into a simple Telegram-friendly response.
6. User can go back to the main menu at any time.

## Free-first architecture

```text
Telegram User
    ↓
Telegram Bot Buttons
    ↓
Python Bot App
    ↓
Handlers
    ├── Start/Menu
    ├── Prices
    ├── Search
    ├── Market Dashboard
    ├── Ask AI
    └── Help
    ↓
Services
    ├── CoinGecko Service
    ├── Groq Service
    └── Formatter Service
```

## Project structure

```text
bot/
├── config.py
├── constants.py
├── main.py
├── handlers/
├── keyboards/
└── services/
run.py
requirements.txt
.env.example
```

## Setup

1. Create a Telegram bot with BotFather and copy the token.
2. Create a free Groq Cloud API key.
3. Copy `.env.example` to `.env`.
4. Fill in your keys.
5. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

6. Run the bot:

```bash
python run.py
```

## Environment variables

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
DEFAULT_CURRENCY=usd
```

## Safety position

This bot is for educational and informational use. It should not guarantee profits, provide private-key handling, custody funds, or claim to provide financial advice.
