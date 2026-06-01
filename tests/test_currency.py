"""测试汇率 API 代理"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_currency_rates_returns_200():
    """GET /api/currency/rates 返回 200 且包含目标货币"""
    response = client.get("/api/currency/rates?base=CNY")
    assert response.status_code == 200
    data = response.json()
    assert "rates" in data
    assert "source" in data
    # 至少包含 4 种目标货币
    targets = ["KZT", "RUB", "USD", "EUR"]
    for code in targets:
        assert code in data["rates"]


def test_currency_rates_default_base_is_cny():
    """不指定 base 参数时默认 CNY"""
    response = client.get("/api/currency/rates")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "CNY"


def test_currency_rates_unsupported_base_returns_422():
    """不支持的货币代码返回 422"""
    response = client.get("/api/currency/rates?base=XXX")
    assert response.status_code == 422


def test_currency_convert():
    """GET /api/currency/convert 正确换算金额"""
    response = client.get("/api/currency/convert?from=CNY&to=KZT&amount=100")
    assert response.status_code == 200
    data = response.json()
    assert data["from"] == "CNY"
    assert data["to"] == "KZT"
    assert data["amount"] == 100.0
    assert isinstance(data["result"], (int, float))
    assert data["rate"] > 0
