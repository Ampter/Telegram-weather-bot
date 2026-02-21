import pytest
from aiohttp import web
from src.bot.main import health_check

@pytest.mark.asyncio
async def test_health_check():
    request = MagicMock()
    response = await health_check(request)
    assert response.status == 200
    assert response.text == "OK"

from unittest.mock import MagicMock
