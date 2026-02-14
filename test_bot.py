from unittest.mock import MagicMock, patch

from bot import get_weather, weather_command


class DummyUpdate:
    def __init__(self):
        self.message = MagicMock()
        self.message.reply_text = MagicMock()


class DummyContext:
    def __init__(self, args):
        self.args = args


@patch("bot.requests.get")
def test_get_weather_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20, "feels_like": 18},
    }

    with patch("bot.OPENWEATHER_API_KEY", "test-key"):
        result = get_weather("London")

    assert "Weather in London" in result
    assert "Clear sky" in result
    assert "Temperature: 20°C (feels like 18°C)" in result


@patch("bot.requests.get")
def test_get_weather_city_not_found(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"message": "city not found"}

    with patch("bot.OPENWEATHER_API_KEY", "test-key"):
        result = get_weather("FakeCity")

    assert "not found" in result.lower()


def test_weather_command_valid_city():
    update = DummyUpdate()
    context = DummyContext(["London"])

    with patch("bot.get_weather", return_value="Weather in London: Clear sky"):
        weather_command(update, context)

    update.message.reply_text.assert_called_once_with("Weather in London: Clear sky")


def test_weather_command_no_city():
    update = DummyUpdate()
    context = DummyContext([])

    weather_command(update, context)

    update.message.reply_text.assert_called_once_with("Usage: /weather <city>")
