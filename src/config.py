import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "10000"))

    def validate(self):
        missing = []
        if not self.TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not self.OPENWEATHER_API_KEY:
            missing.append("OPENWEATHER_API_KEY")
        # DATABASE_URL is optional for local dev if we fall back to in-memory,
        # but let's make it mandatory for production
        if os.getenv("ENVIRONMENT") == "production" and not self.DATABASE_URL:
            missing.append("DATABASE_URL")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

config = Config()
