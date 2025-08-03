"""
Telegram Mini App integration for weather queries.
This class provides a simple interface for the Telegram bot to use as a mini app.
"""
from bot import get_weather

class TelegramMiniApp:
    def __init__(self):
        self.last_location = None
        self.last_weather = None

    def set_location(self, location: str):
        """Set the user's location for weather queries."""
        self.last_location = location
        return f"Location set to: {location}"

    def fetch_weather(self):
        """Fetch weather for the last set location using get_weather from bot.py."""
        if not self.last_location:
            return "No location set. Please set a location first."
        self.last_weather = get_weather(self.last_location)
        return self.last_weather

    def render_ui(self):
        """Return a simple text UI for the mini app (placeholder for real UI)."""
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
