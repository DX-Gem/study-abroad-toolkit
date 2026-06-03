"""留学工具箱 — 后端 API 入口"""
import os
from fastapi import FastAPI, HTTPException, Header
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


# ── 社交模块 API ──────────────────────────────────────

import backend.social as social

# 启动时自动建表
social.init_db()


class AuthBody(BaseModel):
    email: str
    password: str
    name: str = ""


class ProfileBody(BaseModel):
    name: str = None
    avatar: str = None
    school: str = None
    bio: str = None


class PostBody(BaseModel):
    text: str
    topic: str = ""
    images: list = []


class CommentBody(BaseModel):
    text: str


@app.post("/api/auth/register")
async def api_register(body: AuthBody):
    return social.register_user(body.email, body.password, body.name)


@app.post("/api/auth/login")
async def api_login(body: AuthBody):
    return social.login_user(body.email, body.password)


@app.get("/api/auth/me")
async def api_me(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    user = social.require_user(token)
    return {"user": {k: user[k] for k in ["id", "email", "name", "avatar", "school", "bio"]}}


@app.post("/api/auth/profile")
async def api_profile(body: ProfileBody, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.update_profile(token, body.name, body.avatar, body.school, body.bio)


@app.post("/api/posts")
async def api_create_post(body: PostBody, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.create_post(token, body.text, body.topic, body.images)


@app.get("/api/posts")
async def api_list_posts(topic: str = "", page: int = 1, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "").strip() or None
    return social.list_posts(token, topic, page)


@app.delete("/api/posts/{post_id}")
async def api_delete_post(post_id: str, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.delete_post(token, post_id)


@app.post("/api/posts/{post_id}/comments")
async def api_add_comment(post_id: str, body: CommentBody, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.add_comment(token, post_id, body.text)


@app.get("/api/posts/{post_id}/comments")
async def api_list_comments(post_id: str):
    return {"comments": social.list_comments(post_id)}


@app.post("/api/posts/{post_id}/like")
async def api_toggle_like(post_id: str, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.toggle_like(token, post_id)


@app.post("/api/friends/request")
async def api_send_request(body: dict, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.send_friend_request(token, body.get("email", ""))


@app.post("/api/friends/accept")
async def api_accept_request(body: dict, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.accept_friend_request(token, body.get("friend_id", ""))


@app.post("/api/friends/reject")
async def api_reject_request(body: dict, authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.reject_friend_request(token, body.get("friend_id", ""))


@app.get("/api/friends")
async def api_list_friends(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.list_friends(token)


@app.get("/api/users/search")
async def api_search_users(q: str = "", authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    return social.search_users(token, q)


# 托管前端静态文件（本地 + Vercel 统一走这里）
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
