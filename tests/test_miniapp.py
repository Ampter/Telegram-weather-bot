import pytest
from unittest.mock import AsyncMock, MagicMock
from src.miniapp.app import TelegramMiniApp
from src.weather.models import WeatherData

@pytest.mark.asyncio
async def test_miniapp_flow():
    mock_weather_client = MagicMock()
    app = TelegramMiniApp(mock_weather_client)
    user_id = 123

    # Test set_user_city
    res = app.set_user_city(user_id, "Paris")
    assert "Default city set to: Paris" in res
    assert app.get_user_city(user_id) == "Paris"

    # Test fetch_weather success
    mock_weather = WeatherData(city="Paris", description="clear sky", temperature=20, feels_like=18)
    mock_weather_client.get_current_weather = AsyncMock(return_value=mock_weather)

    res = await app.fetch_weather(user_id)
    assert "Weather in Paris" in res
    assert app.last_weather[user_id] == res

    # Test render_ui
    ui = app.render_ui(user_id)
    assert "Default city: Paris" in ui
    assert "Last Weather: Weather in Paris" in ui

@pytest.mark.asyncio
async def test_fetch_weather_no_city():
    app = TelegramMiniApp(MagicMock())
    res = await app.fetch_weather(456)
    assert "No default city set" in res
