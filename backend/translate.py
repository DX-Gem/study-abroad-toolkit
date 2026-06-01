"""翻译 API 代理 — 调用 MyMemory 免费翻译 API"""
import httpx

MYMEMORY_URL = "https://api.mymemory.translated.net/get"

LANG_MAP = {
    "zh": "zh-CN",
    "ru": "ru-RU",
    "kk": "kk-KZ",
}

SUPPORTED_LANGS = [
    {"code": "zh", "name": "中文", "flag": "🇨🇳"},
    {"code": "ru", "name": "俄语", "flag": "🇷🇺"},
    {"code": "kk", "name": "哈语", "flag": "🇰🇿"},
]


async def translate_text(text: str, from_lang: str, to_lang: str) -> dict:
    """翻译文本"""
    from_code = LANG_MAP.get(from_lang, from_lang)
    to_code = LANG_MAP.get(to_lang, to_lang)
    lang_pair = f"{from_code}|{to_code}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            MYMEMORY_URL,
            params={"q": text, "langpair": lang_pair},
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()

    response_data = data.get("responseData", {})
    return {
        "translated": response_data.get("translatedText", ""),
        "match": response_data.get("match", 0),
    }
