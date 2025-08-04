"""
weather_utils.py - Utility functions for weather data retrieval.

This module provides the get_weather function for fetching weather information from OpenWeatherMap.
"""
import os
import requests

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str):
    """Fetch current weather for the given city using OpenWeatherMap API."""
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not set."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return data.get("message", "Failed to get weather data.")
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"Weather in {city.title()}: {weather}\nTemperature: {temp}°C (feels like {feels_like}°C)"
    except Exception as e:
        return f"Error fetching weather: {e}"
