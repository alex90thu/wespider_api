import pytest
from httpx import AsyncClient
from wespider_api.wespider_api.app import app

@pytest.mark.asyncio
async def test_summarize(monkeypatch):
    async def fake_get_wexin_article(query, top_num=5, max_age_days=14):
        return [
            {"title": "Recent 1", "url": "http://example.com/1", "source": "S1", "date": "2025-12-30 12:00:00"},
            {"title": "Recent 2", "url": "http://example.com/2", "source": "S2", "date": "2025-12-29 12:00:00"}
        ]

    monkeypatch.setattr('wespider_api.wespider_api.app.get_wexin_article', fake_get_wexin_article)

    async with AsyncClient(app=app, base_url='http://test') as client:
        resp = await client.post('/summarize', json={"query":"AI","top":2,"max_age_days":14})
        assert resp.status_code == 200
        data = resp.json()
        assert data['count'] == 2
        assert isinstance(data['articles'], list)
