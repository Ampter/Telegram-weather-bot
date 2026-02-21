from typing import Optional
from src.weather.client import WeatherClient

class TelegramMiniApp:
    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client
        self.last_location: Optional[str] = None
        self.last_weather: Optional[str] = None

    def set_location(self, location: str) -> str:
        self.last_location = location
        return f"Location set to: {location}"

    async def fetch_weather(self) -> str:
        if not self.last_location:
            return "No location set. Please set a location first."

        weather = await self.weather_client.get_current_weather(self.last_location)
        if weather:
            self.last_weather = weather.format()
            return self.last_weather
        return "Failed to fetch weather data."

    def render_ui(self) -> str:
        ui = "Telegram Weather Mini App\n"
        if self.last_location:
            ui += f"Current location: {self.last_location}\n"
        else:
            ui += "No location set.\n"

        if self.last_weather:
            ui += f"Weather: {self.last_weather}\n"
        else:
            ui += "No weather data.\n"

        ui += "\nCommands:\n- set_location(<city>)\n- fetch_weather()\n- render_ui()\n"
        return ui
