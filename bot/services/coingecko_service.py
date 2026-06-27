"""CoinGecko API client for free-first crypto market data."""

from __future__ import annotations

import time
from typing import Any

import httpx

from bot.constants import POPULAR_COINS


class CoinGeckoService:
    def __init__(self, base_url: str, currency: str = "usd") -> None:
        self.base_url = base_url
        self.currency = currency
        self._cache: dict[str, tuple[float, Any]] = {}
        self._cache_ttl_seconds = 60

    async def search_coins(self, query: str) -> list[dict[str, Any]]:
        cache_key = f"search:{query.lower()}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._get("/search", params={"query": query})
        coins = data.get("coins", [])[:10]
        self._set_cached(cache_key, coins)
        return coins

    async def get_coin_market_data(self, coin_id: str) -> dict[str, Any]:
        cache_key = f"coin:{coin_id}:{self.currency}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        params = {
            "vs_currency": self.currency,
            "ids": coin_id,
            "order": "market_cap_desc",
            "per_page": 1,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        }
        data = await self._get("/coins/markets", params=params)
        if not data:
            raise ValueError(f"No market data found for {coin_id}.")

        result = data[0]
        self._set_cached(cache_key, result)
        return result

    async def get_popular_market_data(self) -> list[dict[str, Any]]:
        coin_ids = ",".join(POPULAR_COINS.keys())
        cache_key = f"popular:{coin_ids}:{self.currency}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        params = {
            "vs_currency": self.currency,
            "ids": coin_ids,
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        }
        result = await self._get("/coins/markets", params=params)
        self._set_cached(cache_key, result)
        return result

    async def get_global_market_data(self) -> dict[str, Any]:
        cache_key = "global"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        result = await self._get("/global", params={})
        data = result.get("data", {})
        self._set_cached(cache_key, data)
        return data

    async def get_top_movers(self, limit: int = 50) -> dict[str, list[dict[str, Any]]]:
        cache_key = f"top-movers:{self.currency}:{limit}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        params = {
            "vs_currency": self.currency,
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h",
        }
        coins = await self._get("/coins/markets", params=params)
        sortable = [
            coin
            for coin in coins
            if coin.get("price_change_percentage_24h") is not None
        ]
        gainers = sorted(
            sortable, key=lambda coin: coin["price_change_percentage_24h"], reverse=True
        )[:5]
        losers = sorted(sortable, key=lambda coin: coin["price_change_percentage_24h"])[:5]
        result = {"gainers": gainers, "losers": losers}
        self._set_cached(cache_key, result)
        return result

    async def get_trending_coins(self) -> list[dict[str, Any]]:
        cache_key = "trending"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._get("/search/trending", params={})
        trending = [item.get("item", {}) for item in data.get("coins", [])[:7]]
        self._set_cached(cache_key, trending)
        return trending

    async def _get(self, path: str, params: dict[str, Any]) -> Any:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}{path}", params=params)
            response.raise_for_status()
            return response.json()

    def _get_cached(self, key: str) -> Any | None:
        cached = self._cache.get(key)
        if cached is None:
            return None
        cached_at, value = cached
        if time.time() - cached_at > self._cache_ttl_seconds:
            self._cache.pop(key, None)
            return None
        return value

    def _set_cached(self, key: str, value: Any) -> None:
        self._cache[key] = (time.time(), value)
