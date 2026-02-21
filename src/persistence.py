import os
import logging
from typing import Dict, Any, Optional
from telegram.ext import BasePersistence, PersistenceInput

logger = logging.getLogger(__name__)

class TextFilePersistence(BasePersistence):
    """Custom persistence class that stores user cities in a text file: user_id;city"""

    def __init__(self, filepath: str):
        # In PTB v20+, we pass PersistenceInput to super().__init__ or set the attributes
        super().__init__(store_data=PersistenceInput(user_data=True))
        self.filepath = filepath
        self.user_data: Dict[int, Dict[str, Any]] = {}
        logger.info(f"TextFilePersistence initialized with path: {filepath}")
        self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            logger.info(f"Persistence file {self.filepath} not found. Starting fresh.")
            return

        try:
            count = 0
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or ';' not in line:
                        continue
                    try:
                        user_id_str, city = line.split(';', 1)
                        user_id = int(user_id_str)
                        self.user_data[user_id] = {'city': city}
                        count += 1
                    except ValueError:
                        logger.warning(f"Malformed line in persistence file: {line}")
                        continue
            logger.info(f"Loaded {count} users from {self.filepath}")
        except Exception as e:
            logger.error(f"Error loading persistence file: {e}")

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                for user_id, data in self.user_data.items():
                    city = data.get('city')
                    if city:
                        f.write(f"{user_id};{city}\n")
            logger.debug(f"Saved {len(self.user_data)} users to {self.filepath}")
        except Exception as e:
            logger.error(f"Error saving persistence file: {e}")

    async def get_user_data(self) -> Dict[int, Dict[Any, Any]]:
        return self.user_data.copy()

    async def update_user_data(self, user_id: int, data: Dict[Any, Any]) -> None:
        self.user_data[user_id] = data
        self._save()

    async def get_chat_data(self) -> Dict[int, Dict[Any, Any]]:
        return {}

    async def update_chat_data(self, chat_id: int, data: Dict[Any, Any]) -> None:
        pass

    async def get_bot_data(self) -> Dict[Any, Any]:
        return {}

    async def update_bot_data(self, data: Dict[Any, Any]) -> None:
        pass

    async def get_callback_data(self) -> Optional[Dict[Any, Any]]:
        return None

    async def update_callback_data(self, data: Dict[Any, Any]) -> None:
        pass

    async def get_conversations(self, name: str) -> Dict[Any, Any]:
        return {}

    async def update_conversation(self, name: str, key: Any, new_state: Optional[Any]) -> None:
        pass

    async def flush(self) -> None:
        self._save()

    async def drop_chat_data(self, chat_id: int) -> None:
        pass

    async def drop_user_data(self, user_id: int) -> None:
        if user_id in self.user_data:
            del self.user_data[user_id]
            self._save()

    async def refresh_bot_data(self, data: Dict[str, Any]) -> None:
        pass

    async def refresh_chat_data(self, chat_id: int, data: Dict[str, Any]) -> None:
        pass

    async def refresh_user_data(self, user_id: int, data: Dict[str, Any]) -> None:
        pass
