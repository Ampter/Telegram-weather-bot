import pytest
from unittest.mock import AsyncMock, MagicMock
from src.miniapp.app import TelegramMiniApp
from src.weather.models import WeatherData

@pytest.mark.asyncio
async def test_miniapp_flow():
    mock_weather_client = MagicMock()
    app = TelegramMiniApp(mock_weather_client)

    # Test set_location
    res = app.set_location("Paris")
    assert res == "Location set to: Paris"
    assert app.last_location == "Paris"

    # Test fetch_weather success
    mock_weather = WeatherData(city="Paris", description="clear sky", temperature=20, feels_like=18)
    mock_weather_client.get_current_weather = AsyncMock(return_value=mock_weather)

    res = await app.fetch_weather()
    assert "Weather in Paris" in res
    assert app.last_weather == res

    # Test render_ui
    ui = app.render_ui()
    assert "Current location: Paris" in ui
    assert "Weather: Weather in Paris" in ui

@pytest.mark.asyncio
async def test_fetch_weather_no_location():
    app = TelegramMiniApp(MagicMock())
    res = await app.fetch_weather()
    assert res == "No location set. Please set a location first."
