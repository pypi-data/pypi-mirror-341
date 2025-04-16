"""Tests for storage backends."""

from typing import Any, Dict

import pytest

from taskflow.storage import JSONStorage, SQLiteStorage, StorageBackend


@pytest.mark.parametrize("storage", ["json_storage", "sqlite_storage"])
def test_storage_save_and_load(storage: str, request: Any) -> None:
    """Test saving and loading data."""
    backend: StorageBackend = request.getfixturevalue(storage)
    test_data = {"key1": "value1", "key2": {"nested": "value2"}}

    backend.save(test_data)
    loaded_data = backend.load()

    assert loaded_data == test_data


@pytest.mark.parametrize("storage", ["json_storage", "sqlite_storage"])
def test_storage_update(storage: str, request: Any) -> None:
    """Test updating specific keys."""
    backend: StorageBackend = request.getfixturevalue(storage)

    backend.update("test_key", "test_value")
    assert backend.get("test_key") == "test_value"

    backend.update("test_key", "new_value")
    assert backend.get("test_key") == "new_value"


@pytest.mark.parametrize("storage", ["json_storage", "sqlite_storage"])
def test_storage_delete(storage: str, request: Any) -> None:
    """Test deleting keys."""
    backend: StorageBackend = request.getfixturevalue(storage)

    backend.update("test_key", "test_value")
    assert "test_key" in backend.list_keys()

    backend.delete("test_key")
    assert "test_key" not in backend.list_keys()
    assert backend.get("test_key") is None


@pytest.mark.parametrize("storage", ["json_storage", "sqlite_storage"])
def test_storage_list_keys(storage: str, request: Any) -> None:
    """Test listing keys."""
    backend: StorageBackend = request.getfixturevalue(storage)
    test_data = {"key1": "value1", "key2": "value2"}

    backend.save(test_data)
    keys = backend.list_keys()

    assert sorted(keys) == sorted(test_data.keys())


@pytest.mark.parametrize("storage", ["json_storage", "sqlite_storage"])
def test_storage_get_nonexistent(storage: str, request: Any) -> None:
    """Test getting nonexistent key."""
    backend: StorageBackend = request.getfixturevalue(storage)
    assert backend.get("nonexistent") is None


def test_json_storage_creates_path(temp_dir: Any) -> None:
    """Test that JSONStorage creates directory structure."""
    path = temp_dir / "nested" / "path" / "data.json"
    storage = JSONStorage({"path": str(path)})

    assert path.parent.exists()
    assert path.exists()


def test_sqlite_storage_creates_path(temp_dir: Any) -> None:
    """Test that SQLiteStorage creates directory structure."""
    path = temp_dir / "nested" / "path" / "data.db"
    storage = SQLiteStorage({"path": str(path)})

    assert path.parent.exists()
    assert path.exists()
