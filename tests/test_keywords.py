import pytest
from src.persistence import TextFilePersistence

@pytest.mark.asyncio
async def test_refresh_user_data_keywords():
    persistence = TextFilePersistence("dummy.txt")
    # This should not raise TypeError if keywords match
    await persistence.refresh_user_data(user_id=123, user_data={'city': 'Berlin'})

@pytest.mark.asyncio
async def test_refresh_chat_data_keywords():
    persistence = TextFilePersistence("dummy.txt")
    await persistence.refresh_chat_data(chat_id=123, chat_data={})

@pytest.mark.asyncio
async def test_refresh_bot_data_keywords():
    persistence = TextFilePersistence("dummy.txt")
    await persistence.refresh_bot_data(bot_data={})

@pytest.mark.asyncio
async def test_update_conversation_keywords():
    persistence = TextFilePersistence("dummy.txt")
    await persistence.update_conversation(name="test", key="key", new_state="state")
