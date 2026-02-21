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
            "Welcome to the Weather Bot! Use /weather <city> to get the current weather. "
            "Use /forecast <city> for a 3-day forecast. Use /miniapp for the mini app interface."
        )

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send current weather for a specific city."""
        if not context.args:
            await update.message.reply_text("Usage: /weather <city>")
            return

        city = " ".join(context.args)
        weather = await self.weather_client.get_current_weather(city)

        if weather:
            await update.message.reply_text(weather.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find weather data for {city}.")

    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send 3-day forecast for a specific city."""
        if not context.args:
            await update.message.reply_text("Usage: /forecast <city>")
            return

        city = " ".join(context.args)
        forecast = await self.weather_client.get_forecast(city)

        if forecast:
            await update.message.reply_text(forecast.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find forecast data for {city}.")

    async def miniapp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simulate a Mini App interface via bot commands."""
        if not context.args:
            await update.message.reply_text(self.mini_app.render_ui())
            return

        action = context.args[0]
        if action == "set_location":
            if len(context.args) < 2:
                await update.message.reply_text("Usage: /miniapp set_location <city>")
                return
            location = " ".join(context.args[1:])
            result = self.mini_app.set_location(location)
            await update.message.reply_text(result)
        elif action == "fetch_weather":
            result = await self.mini_app.fetch_weather()
            await update.message.reply_text(result)
        else:
            await update.message.reply_text(self.mini_app.render_ui())
