"""留学工具箱 — 后端 API 入口"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Study Abroad Toolkit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy"}


from backend.currency import (
    SUPPORTED_CURRENCIES,
    fetch_rates,
    convert_currency,
)

from backend.translate import translate_text, SUPPORTED_LANGS


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


class TranslateRequest(BaseModel):
    text: str
    from_lang: str = "zh"
    to_lang: str = "ru"


@app.get("/api/translate/langs")
async def get_translate_langs():
    """获取支持的翻译语言列表"""
    return {"langs": SUPPORTED_LANGS}


@app.post("/api/translate")
async def translate_endpoint(body: TranslateRequest):
    """翻译文本"""
    text = body.text.strip()
    from_lang = body.from_lang
    to_lang = body.to_lang

    if not text:
        raise HTTPException(status_code=422, detail="Text is required")

    valid = {lang["code"] for lang in SUPPORTED_LANGS}
    if from_lang not in valid or to_lang not in valid:
        raise HTTPException(status_code=422, detail=f"Unsupported language pair: {from_lang}→{to_lang}")

    result = await translate_text(text, from_lang, to_lang)
    return {
        "text": text,
        "from": from_lang,
        "to": to_lang,
        "result": result["translated"],
        "match": result["match"],
    }


# 托管前端静态文件（本地 + Vercel 统一走这里）
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
