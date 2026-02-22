import os
import asyncio
import pytest
from src.persistence import TextFilePersistence


@pytest.mark.asyncio
async def test_text_file_persistence(tmp_path):
    db_file = tmp_path / "users.txt"
    persistence = TextFilePersistence(str(db_file))

    data = await persistence.get_user_data()
    assert data == {}

    await persistence.update_user_data(123, {"city": "Berlin"})
    assert not os.path.exists(db_file)

    await persistence.flush()

    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        content = f.read()
        assert content == "123;Berlin\n"

    new_persistence = TextFilePersistence(str(db_file))
    loaded_data = await new_persistence.get_user_data()
    assert loaded_data[123]["city"] == "Berlin"


@pytest.mark.asyncio
async def test_text_file_persistence_malformed_lines(tmp_path):
    db_file = tmp_path / "malformed.txt"
    with open(db_file, 'w') as f:
        f.write("abc;city\n")
        f.write("456\n")
        f.write("789;London\n")

    persistence = TextFilePersistence(str(db_file))
    data = await persistence.get_user_data()
    assert len(data) == 1
    assert data[789]["city"] == "London"


@pytest.mark.asyncio
async def test_drop_user_data_is_persisted_on_flush(tmp_path):
    db_file = tmp_path / "users_drop.txt"
    persistence = TextFilePersistence(str(db_file))

    await persistence.update_user_data(123, {"city": "Berlin"})
    await persistence.update_user_data(456, {"city": "Paris"})
    await persistence.flush()

    await persistence.drop_user_data(123)

    reloaded_before_flush = TextFilePersistence(str(db_file))
    data_before = await reloaded_before_flush.get_user_data()
    assert 123 in data_before
    assert 456 in data_before

    await persistence.flush()

    reloaded_after_flush = TextFilePersistence(str(db_file))
    data_after = await reloaded_after_flush.get_user_data()
    assert 123 not in data_after
    assert data_after[456]["city"] == "Paris"


@pytest.mark.asyncio
async def test_periodic_flush_persists_without_manual_flush(tmp_path):
    db_file = tmp_path / "users_periodic.txt"
    persistence = TextFilePersistence(str(db_file), flush_interval_seconds=0.05)

    await persistence.update_user_data(123, {"city": "Berlin"})

    for _ in range(10):
        if os.path.exists(db_file):
            break
        await asyncio.sleep(0.03)

    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        assert f.read() == "123;Berlin\n"

    persistence.stop()
