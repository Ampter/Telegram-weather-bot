import pytest
import os
import asyncio
from src.persistence import TextFilePersistence


def test_text_file_persistence(tmp_path):
    db_file = tmp_path / "users.txt"
    persistence = TextFilePersistence(str(db_file))

    # Test initial state
    data = asyncio.run(persistence.get_user_data())
    assert data == {}

    # Test update without immediate save
    asyncio.run(persistence.update_user_data(123, {"city": "Berlin"}))
    assert not os.path.exists(db_file)

    # Flush persists pending changes
    asyncio.run(persistence.flush())

    # Check if file exists and has correct content
    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        content = f.read()
        assert content == "123;Berlin\n"

    # Test load
    new_persistence = TextFilePersistence(str(db_file))
    loaded_data = asyncio.run(new_persistence.get_user_data())
    assert loaded_data[123]["city"] == "Berlin"


def test_text_file_persistence_malformed_lines(tmp_path):
    db_file = tmp_path / "malformed.txt"
    with open(db_file, 'w') as f:
        f.write("abc;city\n")  # invalid id
        f.write("456\n")     # no separator
        f.write("789;London\n")

    persistence = TextFilePersistence(str(db_file))
    data = asyncio.run(persistence.get_user_data())
    assert len(data) == 1
    assert data[789]["city"] == "London"


def test_drop_user_data_is_persisted_on_flush(tmp_path):
    db_file = tmp_path / "users_drop.txt"
    persistence = TextFilePersistence(str(db_file))

    asyncio.run(persistence.update_user_data(123, {"city": "Berlin"}))
    asyncio.run(persistence.update_user_data(456, {"city": "Paris"}))
    asyncio.run(persistence.flush())

    asyncio.run(persistence.drop_user_data(123))

    # deletion is cached until flush boundary
    reloaded_before_flush = TextFilePersistence(str(db_file))
    data_before = asyncio.run(reloaded_before_flush.get_user_data())
    assert 123 in data_before
    assert 456 in data_before

    asyncio.run(persistence.flush())

    reloaded_after_flush = TextFilePersistence(str(db_file))
    data_after = asyncio.run(reloaded_after_flush.get_user_data())
    assert 123 not in data_after
    assert data_after[456]["city"] == "Paris"
