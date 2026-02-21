import pytest
import os
from src.persistence import TextFilePersistence

@pytest.mark.asyncio
async def test_text_file_persistence(tmp_path):
    db_file = tmp_path / "users.txt"
    persistence = TextFilePersistence(str(db_file))

    # Test initial state
    data = await persistence.get_user_data()
    assert data == {}

    # Test update and save
    await persistence.update_user_data(123, {"city": "Berlin"})

    # Check if file exists and has correct content
    assert os.path.exists(db_file)
    with open(db_file, 'r') as f:
        content = f.read()
        assert content == "123;Berlin\n"

    # Test load
    new_persistence = TextFilePersistence(str(db_file))
    loaded_data = await new_persistence.get_user_data()
    assert loaded_data[123]["city"] == "Berlin"

@pytest.mark.asyncio
async def test_text_file_persistence_malformed_lines(tmp_path):
    db_file = tmp_path / "malformed.txt"
    with open(db_file, 'w') as f:
        f.write("abc;city\n") # invalid id
        f.write("456\n")     # no separator
        f.write("789;London\n")

    persistence = TextFilePersistence(str(db_file))
    data = await persistence.get_user_data()
    assert len(data) == 1
    assert data[789]["city"] == "London"
