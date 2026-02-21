import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "8000"))

    def validate(self):
        missing = []
        if not self.TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not self.OPENWEATHER_API_KEY:
            missing.append("OPENWEATHER_API_KEY")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

config = Config()
