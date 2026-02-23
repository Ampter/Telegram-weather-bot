import pytest
from unittest.mock import AsyncMock
from src.weather.client import WeatherClient


@pytest.mark.asyncio
async def test_weather_client_aclose_signature():
    client = WeatherClient(api_key="dummy")
    # This simulates how PTB calls post_shutdown callbacks
    # It should not raise TypeError
    await client.aclose(object())
