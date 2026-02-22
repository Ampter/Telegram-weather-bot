import logging
import uuid
import asyncio
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from src.weather.client import WeatherClient

logger = logging.getLogger(__name__)


class Handlers:
    """Class containing all Telegram command handlers."""

    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        user_id = update.effective_user.id if update.effective_user else "Unknown"
        logger.debug(f"User {user_id} triggered /start")
        await update.effective_message.reply_text(
            "Welcome to the Weather Bot!\n\n"
            "Commands:\n"
            "/set_city <city> - Set your default city (e.g., /set_city Kaliningrad)\n"
            "/weather [city] - Get weather for [city] or your default city\n"
            "/forecast [city] - Get 3-day forecast"
        )
        logger.debug(f"/start handled for user {user_id}")

    async def set_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the default city for the user."""
        user_id = update.effective_user.id if update.effective_user else "Unknown"
        logger.debug(f"User {user_id} triggered /set_city")
        if not context.args:
            await update.effective_message.reply_text("Usage: /set_city <city>")
            return

        city = " ".join(context.args)
        context.user_data['city'] = city
        await update.effective_message.reply_text(f"Default city set to: {city}")
        logger.debug(f"/set_city handled for user {user_id}: {city}")

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send current weather."""
        user_id = update.effective_user.id if update.effective_user else "Unknown"
        logger.debug(f"User {user_id} triggered /weather")
        city = " ".join(
            context.args) if context.args else context.user_data.get('city')

        if not city:
            await update.effective_message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        weather = await self.weather_client.get_current_weather(city)
        if weather:
            await update.effective_message.reply_text(weather.format())
        else:
            await update.effective_message.reply_text(f"Sorry, I couldn't find weather data for {city}.")
        logger.debug(f"/weather handled for user {user_id} and city {city}")

    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send 3-day forecast."""
        user_id = update.effective_user.id if update.effective_user else "Unknown"
        logger.debug(f"User {user_id} triggered /forecast")
        city = " ".join(
            context.args) if context.args else context.user_data.get('city')

        if not city:
            await update.effective_message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        forecast = await self.weather_client.get_forecast(city)
        if forecast:
            await update.effective_message.reply_text(forecast.format())
        else:
            await update.effective_message.reply_text(f"Sorry, I couldn't find forecast data for {city}.")
        logger.debug(f"/forecast handled for user {user_id} and city {city}")

    async def inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline queries."""
        query = update.inline_query.query
        user_id = update.effective_user.id
        logger.debug(f"User {user_id} triggered inline query: {query}")

        city = query.strip() if query.strip() else context.user_data.get('city')

        if not city:
            # If no city provided and no default city, we can't show much
            return

        results = []

        # Fetch weather and forecast concurrently
        weather, forecast = await asyncio.gather(
            self.weather_client.get_current_weather(city),
            self.weather_client.get_forecast(city)
        )

        if weather:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"Current Weather in {city}",
                    input_message_content=InputTextMessageContent(weather.format()),
                    description=f"Temperature: {weather.temperature}°C, {weather.description}"
                )
            )

        if forecast:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"3-Day Forecast for {city}",
                    input_message_content=InputTextMessageContent(forecast.format()),
                    description="View the 3-day weather outlook"
                )
            )

        await update.inline_query.answer(results, cache_time=300)
