from dataclasses import dataclass
from typing import List

@dataclass
class WeatherData:
    city: str
    description: str
    temperature: float
    feels_like: float

    def format(self) -> str:
        return (
            f"Weather in {self.city.title()}: {self.description.capitalize()}\n"
            f"Temperature: {self.temperature}°C (feels like {self.feels_like}°C)"
        )

@dataclass
class ForecastEntry:
    date: str
    description: str
    temperature: float

@dataclass
class ForecastData:
    city: str
    entries: List[ForecastEntry]

    def format(self) -> str:
        header = f"3-day forecast for {self.city.title()}:\n"
        lines = [f"{e.date}: {e.description.capitalize()}, {e.temperature}°C" for e in self.entries]
        return header + "\n".join(lines)
