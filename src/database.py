import asyncpg
import logging
from src.config import config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not config.DATABASE_URL:
            logger.warning("DATABASE_URL not set. Database operations will be skipped.")
            return False

        try:
            self.pool = await asyncpg.create_pool(config.DATABASE_URL)
            logger.info("Connected to PostgreSQL database.")
            await self.init_db()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False

    async def init_db(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id BIGINT PRIMARY KEY,
                    city TEXT NOT NULL
                );
            """)
            logger.info("Database schema initialized.")

    async def set_user_city(self, user_id: int, city: str):
        if not self.pool:
            return "Database not connected."

        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_preferences (user_id, city)
                VALUES (, )
                ON CONFLICT (user_id) DO UPDATE SET city = EXCLUDED.city;
            """, user_id, city)
            return f"Default city set to: {city}"

    async def get_user_city(self, user_id: int):
        if not self.pool:
            return None

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT city FROM user_preferences WHERE user_id = ", user_id)
            return row['city'] if row else None

    async def close(self):
        if self.pool:
            await self.pool.close()
