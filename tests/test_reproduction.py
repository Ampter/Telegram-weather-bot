import pytest
import os
from telegram.ext import ApplicationBuilder
from src.persistence import TextFilePersistence


@pytest.mark.asyncio
async def test_persistence_integration_with_keywords(tmp_path):
    """Test that persistence methods can be called with keyword arguments, as PTB might do."""
    db_file = tmp_path / "test_data.txt"
    persistence = TextFilePersistence(str(db_file))

    await persistence.update_user_data(user_id=123, data={'city': 'Berlin'})
    user_data = await persistence.get_user_data()
    assert user_data[123] == {'city': 'Berlin'}

    assert not os.path.exists(db_file)
    await persistence.flush()
    assert os.path.exists(db_file)


@pytest.mark.asyncio
async def test_persistence_integration(tmp_path):
    db_file = tmp_path / "users.txt"
    persistence = TextFilePersistence(str(db_file))

    application = (
        ApplicationBuilder()
        .token("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        .persistence(persistence)
        .build()
    )

    await application.persistence.get_user_data()
    await application.persistence.update_user_data(123, {"city": "Berlin"})

    assert not os.path.exists(db_file)

    await application.persistence.flush()
    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        assert f.read() == "123;Berlin\n"
