import pytest
import os
import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from src.persistence import TextFilePersistence

@pytest.mark.asyncio
async def test_persistence_integration_with_keywords():
    """Test that persistence methods can be called with keyword arguments, as PTB might do."""
    persistence = TextFilePersistence("test_data.txt")

    # Test update_user_data with keyword arguments ('data' is what PTB uses)
    await persistence.update_user_data(user_id=123, data={'city': 'Berlin'})
    user_data = await persistence.get_user_data()
    assert user_data[123] == {'city': 'Berlin'}

    # Clean up
    if os.path.exists("test_data.txt"):
        os.remove("test_data.txt")

@pytest.mark.asyncio
async def test_persistence_integration(tmp_path):
    db_file = tmp_path / "users.txt"
    persistence = TextFilePersistence(str(db_file))

    # PTB v20+ Application with persistence
    application = (
        ApplicationBuilder()
        .token("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11") # fake token
        .persistence(persistence)
        .build()
    )

    # Simulate loading data
    # Application.initialize() will call get_user_data, get_chat_data, etc.
    # We can't fully initialize without a real bot token connection if it starts polling,
    # but we can trigger the methods.

    await application.persistence.get_user_data()
    await application.persistence.update_user_data(123, {"city": "Berlin"})

    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        assert f.read() == "123;Berlin\n"
