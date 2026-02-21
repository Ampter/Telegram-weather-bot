import httpx
import logging
from typing import Optional
from itertools import groupby
from .models import WeatherData, ForecastData, ForecastEntry

logger = logging.getLogger(__name__)

class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_current_weather(self, city: str) -> Optional[WeatherData]:
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    return WeatherData(
                        city=city,
                        description=data["weather"][0]["description"],
                        temperature=data["main"]["temp"],
                        feels_like=data["main"]["feels_like"]
                    )
                else:
                    logger.error(f"Error fetching weather for {city}: {response.status_code} {response.text}")
                    return None
        except Exception as e:
            logger.exception(f"Unexpected error fetching weather for {city}")
            return None

    async def get_forecast(self, city: str, days: int = 3) -> Optional[ForecastData]:
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    forecast_list = data.get("list", [])

                    # Group by day
                    key = lambda e: e["dt_txt"].split()[0]
                    grouped = groupby(forecast_list, key)
                    entries = []
                    for _, group in grouped:
                        entry = next(group)
                        entries.append(ForecastEntry(
                            date=entry["dt_txt"].split()[0],
                            description=entry["weather"][0]["description"],
                            temperature=entry["main"]["temp"]
                        ))

                    return ForecastData(city=city, entries=entries[:days])
                else:
                    logger.error(f"Error fetching forecast for {city}: {response.status_code} {response.text}")
                    return None
        except Exception as e:
            logger.exception(f"Unexpected error fetching forecast for {city}")
            return None
