import os
import logging
import threading
from typing import Dict, Any, Optional
from contextlib import suppress
from telegram.ext import BasePersistence

logger = logging.getLogger(__name__)


class TextFilePersistence(BasePersistence):
    """Custom persistence class that stores user cities in a text file: user_id;city"""

    def __init__(self, filepath: str, flush_interval_seconds: Optional[float] = None):
        super().__init__()
        self.filepath = filepath
        self.user_data_cache: Dict[int, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._dirty = False
        self._flush_interval_seconds = flush_interval_seconds
        self._stop_event = threading.Event()
        self._flush_thread: Optional[threading.Thread] = None
        self._load()

        if flush_interval_seconds and flush_interval_seconds > 0:
            self._flush_thread = threading.Thread(
                target=self._periodic_flush_loop,
                name="text-file-persistence-flush",
                daemon=True,
            )
            self._flush_thread.start()

    def _load(self):
        if not os.path.exists(self.filepath):
            logger.info(f"Persistence file not found: {self.filepath}")
            return

        logger.info(f"Loading persistence from {self.filepath}")
        try:
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or ';' not in line:
                        continue
                    try:
                        user_id_str, city = line.split(';', 1)
                        user_id = int(user_id_str)
                        self.user_data_cache[user_id] = {'city': city}
                    except ValueError:
                        continue
            logger.info(
                f"Loaded {len(self.user_data_cache)} users from {self.filepath}")
        except Exception as e:
            logger.error(f"Error loading persistence file: {e}")


    def _periodic_flush_loop(self) -> None:
        while not self._stop_event.wait(self._flush_interval_seconds):
            self._save()

    def stop(self) -> None:
        self._stop_event.set()
        if self._flush_thread and self._flush_thread.is_alive():
            self._flush_thread.join(timeout=1)

    def __del__(self):
        with suppress(Exception):
            self.stop()

    def _save(self, force: bool = False):
        with self._lock:
            if not force and not self._dirty:
                logger.debug("Skipping persistence save: no pending changes")
                return

            logger.debug(f"Saving persistence to {self.filepath}")
            try:
                persistence_dir = os.path.dirname(self.filepath)
                if persistence_dir:
                    os.makedirs(persistence_dir, exist_ok=True)
                with open(self.filepath, 'w') as f:
                    # Use list(items()) to avoid RuntimeError during iteration if modified
                    for user_id, data in list(self.user_data_cache.items()):
                        city = data.get('city')
                        if city:
                            f.write(f"{user_id};{city}\n")
                self._dirty = False
                logger.info(
                    f"Successfully saved persistence to {self.filepath}")
            except Exception as e:
                logger.error(
                    f"Error saving persistence file {self.filepath}: {e}")

    async def get_user_data(self) -> Dict[int, Dict[Any, Any]]:
        logger.debug("Getting user data from persistence")
        with self._lock:
            return self.user_data_cache.copy()

    async def update_user_data(self, user_id: int, data: Dict[Any, Any]) -> None:
        logger.debug(f"Updating user data for {user_id}")
        with self._lock:
            self.user_data_cache[user_id] = data
            self._dirty = True

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

    async def update_callback_data(self, data: Any) -> None:
        pass

    async def get_conversations(self, name: str) -> Dict[Any, Any]:
        return {}

    async def update_conversation(self, name: str, key: Any, new_state: Optional[Any]) -> None:
        pass

    async def flush(self) -> None:
        logger.info("Flushing persistence to disk")
        self._save(force=True)

    async def drop_chat_data(self, chat_id: int) -> None:
        pass

    async def drop_user_data(self, user_id: int) -> None:
        with self._lock:
            if user_id in self.user_data_cache:
                del self.user_data_cache[user_id]
                self._dirty = True

    async def refresh_bot_data(self, bot_data: Dict[str, Any]) -> None:
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: Dict[str, Any]) -> None:
        pass

    async def refresh_user_data(self, user_id: int, user_data: Dict[str, Any]) -> None:
        pass
