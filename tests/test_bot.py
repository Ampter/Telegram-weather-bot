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
    mock.effective_user.id = 123
    return mock

@pytest.mark.asyncio
async def test_start_command(handlers, update):
    await handlers.start(update, None)
    update.message.reply_text.assert_called_once()
    assert "Welcome" in update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_set_city_command(handlers, update, mock_mini_app):
    context = MagicMock()
    context.args = ["Kaliningrad"]
    mock_mini_app.set_user_city.return_value = "Success"

    await handlers.set_city_command(update, context)
    mock_mini_app.set_user_city.assert_called_once_with(123, "Kaliningrad")
    update.message.reply_text.assert_called_once_with("Success")

@pytest.mark.asyncio
async def test_weather_command_with_default(handlers, update, mock_weather_client, mock_mini_app):
    context = MagicMock()
    context.args = []
    mock_mini_app.get_user_city.return_value = "Kaliningrad"

    mock_weather = WeatherData(city="Kaliningrad", description="sunny", temperature=10, feels_like=8)
    mock_weather_client.get_current_weather = AsyncMock(return_value=mock_weather)

    await handlers.weather_command(update, context)
    update.message.reply_text.assert_called_once_with(mock_weather.format())

@pytest.mark.asyncio
async def test_weather_command_no_default_no_args(handlers, update, mock_mini_app):
    context = MagicMock()
    context.args = []
    mock_mini_app.get_user_city.return_value = None

    await handlers.weather_command(update, context)
    update.message.reply_text.assert_called_once_with("Please provide a city or set a default one with /set_city <city>")
