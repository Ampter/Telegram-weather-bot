import os
import pytest
from unittest.mock import patch, MagicMock

# Assume bot.py defines a function get_weather(city) and a function handle_weather_command(update, context)
from bot import get_weather, handle_weather_command

class DummyUpdate:
    def __init__(self):
        self.message = MagicMock()
        self.message.reply_text = MagicMock()

class DummyContext:
    def __init__(self, args):
        self.args = args

@patch('bot.requests.get')
def test_get_weather_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 20, 'humidity': 50},
        'wind': {'speed': 3.5},
        'name': 'London'
    }
    result = get_weather('London')
    assert 'London' in result
    assert 'clear sky' in result
    assert 'Temperature' in result

@patch('bot.requests.get')
def test_get_weather_city_not_found(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {'message': 'city not found'}
    result = get_weather('FakeCity')
    assert 'not found' in result.lower()

@patch('bot.get_weather')
def test_handle_weather_command_valid_city(mock_get_weather):
    mock_get_weather.return_value = 'Weather in London: clear sky, 20°C'
    update = DummyUpdate()
    context = DummyContext(['London'])
    handle_weather_command(update, context)
    update.message.reply_text.assert_called_with('Weather in London: clear sky, 20°C')

@patch('bot.get_weather')
def test_handle_weather_command_no_city(mock_get_weather):
    update = DummyUpdate()
    context = DummyContext([])
    handle_weather_command(update, context)
    update.message.reply_text.assert_called_with('Please provide a city name. Usage: /weather <city>')

@patch('bot.get_weather')
def test_handle_weather_command_api_error(mock_get_weather):
    mock_get_weather.return_value = 'Error: Unable to fetch weather data.'
    update = DummyUpdate()
    context = DummyContext(['London'])
    handle_weather_command(update, context)
    update.message.reply_text.assert_called_with('Error: Unable to fetch weather data.')

# To run these tests: pytest test_bot.py
