import pytest
from unittest.mock import MagicMock, AsyncMock
from src.bot.handlers import Handlers


@pytest.mark.asyncio
async def test_weather_command_no_user():
    handlers = Handlers(MagicMock())
    update = MagicMock()
    update.effective_user = None
    update.effective_message.reply_text = AsyncMock()

    context = MagicMock()
    context.args = []
    context.user_data = None

    # This should not raise AttributeError now
    await handlers.weather_command(update, context)
    update.effective_message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_forecast_command_no_user():
    handlers = Handlers(MagicMock())
    update = MagicMock()
    update.effective_user = None
    update.effective_message.reply_text = AsyncMock()

    context = MagicMock()
    context.args = []
    context.user_data = None

    # This should not raise AttributeError now
    await handlers.forecast_command(update, context)
    update.effective_message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_inline_query_no_user_data():
    handlers = Handlers(MagicMock())
    update = MagicMock()
    update.inline_query.query = ""
    update.inline_query.answer = AsyncMock()
    update.effective_user.id = 123

    context = MagicMock()
    context.user_data = None

    # This should not raise AttributeError now
    await handlers.inline_query(update, context)
    # It should just return without answering if city is None
    update.inline_query.answer.assert_not_called()

@pytest.mark.asyncio
async def test_set_city_command_no_user_data():
    handlers = Handlers(MagicMock())
    update = MagicMock()
    update.effective_user = None
    update.effective_message.reply_text = AsyncMock()

    context = MagicMock()
    context.args = ["London"]
    context.user_data = None

    # This should not raise TypeError anymore
    await handlers.set_city_command(update, context)
    update.effective_message.reply_text.assert_called_once()
    args, _ = update.effective_message.reply_text.call_args
    assert "User data is not available" in args[0]
