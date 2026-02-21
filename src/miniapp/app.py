from typing import Optional, Dict
from src.weather.client import WeatherClient
from src.database import Database

class TelegramMiniApp:
    def __init__(self, weather_client: WeatherClient, db: Database):
        self.weather_client = weather_client
        self.db = db
        self.last_weather: Dict[int, str] = {}

    async def set_user_city(self, user_id: int, city: str) -> str:
        return await self.db.set_user_city(user_id, city)

    async def get_user_city(self, user_id: int) -> Optional[str]:
        return await self.db.get_user_city(user_id)

    async def fetch_weather(self, user_id: int) -> str:
        city = await self.get_user_city(user_id)
        if not city:
            return "No default city set. Please use /set_city <city> first."

        weather = await self.weather_client.get_current_weather(city)
        if weather:
            formatted = weather.format()
            self.last_weather[user_id] = formatted
            return formatted
        return f"Failed to fetch weather data for {city}."

    async def render_ui(self, user_id: int) -> str:
        city = await self.get_user_city(user_id)
        ui = "Telegram Weather Mini App\n"
        if city:
            ui += f"Default city: {city}\n"
        else:
            ui += "No default city set.\n"

        last = self.last_weather.get(user_id)
        if last:
            ui += f"Last Weather: {last}\n"
        else:
            ui += "No weather data fetched yet.\n"

        ui += "\nCommands:\n- /set_city <city>\n- /weather (uses default)\n- /miniapp (shows this UI)\n"
        return ui
