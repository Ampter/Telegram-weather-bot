import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.weather.client import WeatherClient
from src.miniapp.app import TelegramMiniApp

logger = logging.getLogger(__name__)

class Handlers:
    """Class containing all Telegram command handlers."""

    def __init__(self, weather_client: WeatherClient, mini_app: TelegramMiniApp):
        self.weather_client = weather_client
        self.mini_app = mini_app

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        await update.message.reply_text(
            "Welcome to the Weather Bot!\n\n"
            "Commands:\n"
            "/set_city <city> - Set your default city (e.g., /set_city Kaliningrad)\n"
            "/weather [city] - Get weather for [city] or your default city\n"
            "/forecast [city] - Get 3-day forecast\n"
            "/miniapp - Open the mini app interface"
        )

    async def set_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the default city for the user."""
        if not context.args:
            await update.message.reply_text("Usage: /set_city <city>")
            return

        city = " ".join(context.args)
        user_id = update.effective_user.id
        result = self.mini_app.set_user_city(user_id, city)
        await update.message.reply_text(result)

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send current weather."""
        user_id = update.effective_user.id
        city = " ".join(context.args) if context.args else self.mini_app.get_user_city(user_id)

        if not city:
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        weather = await self.weather_client.get_current_weather(city)
        if weather:
            await update.message.reply_text(weather.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find weather data for {city}.")

    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send 3-day forecast."""
        user_id = update.effective_user.id
        city = " ".join(context.args) if context.args else self.mini_app.get_user_city(user_id)

        if not city:
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        forecast = await self.weather_client.get_forecast(city)
        if forecast:
            await update.message.reply_text(forecast.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find forecast data for {city}.")

    async def miniapp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simulate a Mini App interface."""
        user_id = update.effective_user.id

        # If no arguments, show UI
        if not context.args:
            # Auto-fetch weather if default city exists
            if self.mini_app.get_user_city(user_id):
                await self.mini_app.fetch_weather(user_id)
            await update.message.reply_text(self.mini_app.render_ui(user_id))
            return

        action = context.args[0]
        if action == "fetch_weather":
            result = await self.mini_app.fetch_weather(user_id)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text(self.mini_app.render_ui(user_id))
