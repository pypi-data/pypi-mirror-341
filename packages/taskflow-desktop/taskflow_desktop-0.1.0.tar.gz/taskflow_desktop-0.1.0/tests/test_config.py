"""Tests for configuration module."""

from pathlib import Path

import pytest
import yaml

from taskflow.config import Config, StorageConfig, UIConfig


def test_config_loads_correctly(config: Config) -> None:
    """Test if configuration loads correctly."""
    assert config.environment == "test"
    assert isinstance(config.ui, UIConfig)
    assert isinstance(config.storage, StorageConfig)


def test_ui_config_from_dict(config: Config) -> None:
    """Test UIConfig creation from dictionary."""
    ui = config.ui
    assert ui.primary_color == "#007ACC"
    assert ui.secondary_color == "#2C2C2C"
    assert ui.font_family == "Segoe UI"
    assert ui.sidebar_width == 250
    assert ui.toolbar_height == 40


def test_storage_config_from_dict(config: Config) -> None:
    """Test StorageConfig creation from dictionary."""
    storage = config.storage
    assert storage.default_backend == "json"
    assert "json" in storage.backends
    assert "sqlite" in storage.backends


def test_config_missing_file() -> None:
    """Test configuration with missing file."""
    with pytest.raises(FileNotFoundError):
        Config(Path("nonexistent.yaml"))


def test_config_invalid_yaml(temp_dir: Path) -> None:
    """Test configuration with invalid YAML."""
    config_path = temp_dir / "invalid.yaml"
    config_path.write_text("invalid: yaml: content")

    with pytest.raises(yaml.YAMLError):
        Config(config_path)
