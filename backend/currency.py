"""汇率 API 代理 — 调用 exchangerate-api.com"""
import time
from typing import Optional

import httpx

# 支持的货币
SUPPORTED_CURRENCIES = {"CNY", "KZT", "RUB", "USD", "EUR"}

# exchangerate-api.com 免费层：基础货币固定为 USD
# 我们获取 USD 对所有货币的汇率，然后交叉计算
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# 简易缓存：存储最后一次获取的汇率和获取时间
_cache: Optional[dict] = None
_cache_timestamp: float = 0.0
CACHE_TTL_SECONDS = 3600  # 1 小时缓存


async def fetch_rates() -> dict:
    """从 exchangerate-api.com 获取最新汇率（带缓存）"""
    global _cache, _cache_timestamp

    now = time.time()
    if _cache is not None and (now - _cache_timestamp) < CACHE_TTL_SECONDS:
        return _cache

    async with httpx.AsyncClient() as client:
        response = await client.get(EXCHANGE_API_URL, timeout=10.0)
        response.raise_for_status()
        data = response.json()

    if "rates" not in data:
        raise ValueError("Invalid response from exchange rate API")

    _cache = data
    _cache_timestamp = now
    return data


def convert_currency(amount: float, from_cur: str, to_cur: str, rates_query: dict) -> float:
    """利用 USD 中间汇率进行货币换算

    from_cur -> USD -> to_cur
    """
    usd_rates = rates_query["rates"]
    # 先转换成 USD
    amount_in_usd = amount / usd_rates[from_cur]
    # 再从 USD 转换成目标货币
    result = amount_in_usd * usd_rates[to_cur]
    return round(result, 2)
