"""翻译模块测试"""
import pytest
from backend.translate import translate_text, SUPPORTED_LANGS


@pytest.mark.asyncio
async def test_translate_zh_to_ru():
    result = await translate_text("你好", "zh", "ru")
    assert "translated" in result
    assert len(result["translated"]) > 0
    assert "match" in result


@pytest.mark.asyncio
async def test_translate_zh_to_kk():
    result = await translate_text("谢谢", "zh", "kk")
    assert "translated" in result
    assert len(result["translated"]) > 0


@pytest.mark.asyncio
async def test_translate_ru_to_zh():
    result = await translate_text("Здравствуйте", "ru", "zh")
    assert "translated" in result
    assert len(result["translated"]) > 0


def test_supported_langs():
    assert len(SUPPORTED_LANGS) == 3
    for lang in SUPPORTED_LANGS:
        assert "code" in lang
        assert "name" in lang
        assert "flag" in lang
