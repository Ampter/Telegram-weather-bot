import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.weather.client import WeatherClient

@pytest.mark.asyncio
async def test_get_current_weather_success():
    client = WeatherClient("test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20.5, "feels_like": 19.0}
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        weather = await client.get_current_weather("London")

    assert weather is not None
    assert weather.city == "London"
    assert weather.description == "clear sky"
    assert weather.temperature == 20.5
    assert "Weather in London" in weather.format()

@pytest.mark.asyncio
async def test_get_current_weather_failure():
    client = WeatherClient("test_key")

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        weather = await client.get_current_weather("UnknownCity")

    assert weather is None

@pytest.mark.asyncio
async def test_get_forecast_success():
    client = WeatherClient("test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "list": [
            {"dt_txt": "2023-01-01 12:00:00", "weather": [{"description": "sunny"}], "main": {"temp": 25}},
            {"dt_txt": "2023-01-02 12:00:00", "weather": [{"description": "cloudy"}], "main": {"temp": 22}},
            {"dt_txt": "2023-01-03 12:00:00", "weather": [{"description": "rain"}], "main": {"temp": 18}}
        ]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        forecast = await client.get_forecast("London", days=3)

    assert forecast is not None
    assert len(forecast.entries) == 3
    assert forecast.entries[0].description == "sunny"
    assert "3-day forecast" in forecast.format()
