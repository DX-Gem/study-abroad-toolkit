"""留学工具箱 — 后端 API 入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Study Abroad Toolkit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "service": "Study Abroad Toolkit API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


from backend.currency import (
    SUPPORTED_CURRENCIES,
    fetch_rates,
    convert_currency,
)


@app.get("/api/currency/rates")
async def get_currency_rates(base: str = "CNY"):
    """获取目标货币汇率

    Args:
        base: 基准货币代码（默认 CNY）
    """
    base = base.upper()
    if base not in SUPPORTED_CURRENCIES:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Unsupported currency: {base}")

    raw = await fetch_rates()
    all_rates = raw["rates"]

    # 将 USD-based 汇率转换为 base-based 汇率
    base_to_usd = all_rates[base]
    adjusted_rates = {}
    for code in SUPPORTED_CURRENCIES:
        if code == base:
            adjusted_rates[code] = 1.0
        else:
            adjusted_rates[code] = round(all_rates[code] / base_to_usd, 6)

    return {
        "source": base,
        "updated": raw.get("date", "unknown"),
        "rates": adjusted_rates,
    }


@app.get("/api/currency/convert")
async def convert_currency_endpoint(
    from_cur: str = "CNY",
    to: str = "KZT",
    amount: float = 1.0,
):
    """货币换算

    Args:
        from_cur: 源货币代码
        to: 目标货币代码
        amount: 金额
    """
    from_cur = from_cur.upper()
    to = to.upper()

    if from_cur not in SUPPORTED_CURRENCIES:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Unsupported currency: {from_cur}")
    if to not in SUPPORTED_CURRENCIES:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Unsupported currency: {to}")

    raw = await fetch_rates()
    result = convert_currency(amount, from_cur, to, raw)

    return {
        "from": from_cur,
        "to": to,
        "amount": amount,
        "result": result,
        "rate": round(result / amount, 6) if amount else 0,
    }
