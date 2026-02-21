from typing import Optional, Dict
from src.weather.client import WeatherClient

class TelegramMiniApp:
    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client
        self.last_weather: Dict[int, str] = {}

    def set_user_city(self, user_data: Dict, city: str) -> str:
        user_data['city'] = city
        return f"Default city set to: {city}"

    def get_user_city(self, user_data: Dict) -> Optional[str]:
        return user_data.get('city')

    async def fetch_weather(self, user_data: Dict) -> str:
        city = self.get_user_city(user_data)
        if not city:
            return "No default city set. Please use /set_city <city> first."

        weather = await self.weather_client.get_current_weather(city)
        if weather:
            formatted = weather.format()
            # Note: last_weather is still in-memory and not persisted across restarts
            # unless we move it to user_data too. Let's do that for full persistence.
            user_data['last_weather'] = formatted
            return formatted
        return f"Failed to fetch weather data for {city}."

    def render_ui(self, user_data: Dict) -> str:
        city = self.get_user_city(user_data)
        ui = "Telegram Weather Mini App\n"
        if city:
            ui += f"Default city: {city}\n"
        else:
            ui += "No default city set.\n"

        last = user_data.get('last_weather')
        if last:
            ui += f"Last Weather: {last}\n"
        else:
            ui += "No weather data fetched yet.\n"

        ui += "\nCommands:\n- /set_city <city>\n- /weather (uses default)\n- /miniapp (shows this UI)\n"
        return ui
