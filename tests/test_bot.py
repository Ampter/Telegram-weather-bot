import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot.handlers import Handlers
from src.weather.models import WeatherData, ForecastData, ForecastEntry

@pytest.fixture
def mock_weather_client():
    return MagicMock()

@pytest.fixture
def mock_mini_app():
    return MagicMock()

@pytest.fixture
def handlers(mock_weather_client, mock_mini_app):
    return Handlers(mock_weather_client, mock_mini_app)

@pytest.fixture
def update():
    mock = MagicMock()
    mock.message.reply_text = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_start_command(handlers, update):
    await handlers.start(update, None)
    update.message.reply_text.assert_called_once()
    assert "Welcome" in update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_weather_command_success(handlers, update, mock_weather_client):
    context = MagicMock()
    context.args = ["London"]

    mock_weather = WeatherData(city="London", description="sunny", temperature=25, feels_like=24)
    mock_weather_client.get_current_weather = AsyncMock(return_value=mock_weather)

    await handlers.weather_command(update, context)
    update.message.reply_text.assert_called_once_with(mock_weather.format())

@pytest.mark.asyncio
async def test_weather_command_no_args(handlers, update):
    context = MagicMock()
    context.args = []

    await handlers.weather_command(update, context)
    update.message.reply_text.assert_called_once_with("Usage: /weather <city>")

@pytest.mark.asyncio
async def test_forecast_command_success(handlers, update, mock_weather_client):
    context = MagicMock()
    context.args = ["Tokyo"]

    mock_forecast = ForecastData(city="Tokyo", entries=[
        ForecastEntry(date="2023-01-01", description="rain", temperature=15)
    ])
    mock_weather_client.get_forecast = AsyncMock(return_value=mock_forecast)

    await handlers.forecast_command(update, context)
    update.message.reply_text.assert_called_once_with(mock_forecast.format())

@pytest.mark.asyncio
async def test_miniapp_command_render(handlers, update, mock_mini_app):
    context = MagicMock()
    context.args = []
    mock_mini_app.render_ui.return_value = "UI CONTENT"

    await handlers.miniapp_command(update, context)
    update.message.reply_text.assert_called_once_with("UI CONTENT")
