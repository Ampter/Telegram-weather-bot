import pytest
from unittest.mock import AsyncMock, MagicMock
from src.bot.handlers import Handlers
from src.weather.models import WeatherData


@pytest.fixture
def mock_weather_client():
    return MagicMock()


@pytest.fixture
def handlers(mock_weather_client):
    return Handlers(mock_weather_client)


@pytest.fixture
def update():
    mock = MagicMock()
    mock.effective_message.reply_text = AsyncMock()
    mock.message = mock.effective_message
    mock.effective_user.id = 123
    return mock


@pytest.fixture
def context():
    mock = MagicMock()
    mock.user_data = {}
    mock.args = []
    return mock


@pytest.mark.asyncio
async def test_start_command(handlers, update, context):
    await handlers.start(update, context)
    update.effective_message.reply_text.assert_called_once()
    assert "Welcome" in update.effective_message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_set_city_command(handlers, update, context):
    context.args = ["Kaliningrad"]

    await handlers.set_city_command(update, context)
    assert context.user_data['city'] == "Kaliningrad"
    update.effective_message.reply_text.assert_called_once_with(
        "Default city set to: Kaliningrad")


@pytest.mark.asyncio
async def test_weather_command_with_default(handlers, update, context, mock_weather_client):
    context.user_data['city'] = "Kaliningrad"
    mock_weather = WeatherData(
        city="Kaliningrad", description="sunny", temperature=10, feels_like=8)
    mock_weather_client.get_current_weather = AsyncMock(
        return_value=mock_weather)

    await handlers.weather_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        mock_weather.format())


@pytest.mark.asyncio
async def test_weather_command_no_default_no_args(handlers, update, context):
    await handlers.weather_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        "Please provide a city or set a default one with /set_city <city>")


@pytest.mark.asyncio
async def test_error_handler():
    from src.bot.main import error_handler
    from telegram import Update
    update = MagicMock(spec=Update)
    update.effective_message.reply_text = AsyncMock()
    context = MagicMock()
    context.error = Exception("Test error")

    await error_handler(update, context)

    update.effective_message.reply_text.assert_called_once_with(
        "An unexpected error occurred. Please try again later."
    )
