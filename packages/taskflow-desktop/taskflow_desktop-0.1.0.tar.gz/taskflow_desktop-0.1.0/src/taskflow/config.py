"""Configuration management for TaskFlow."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass
class UIConfig:
    """UI configuration settings."""

    primary_color: str
    secondary_color: str
    font_family: str
    sidebar_width: int
    toolbar_height: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UIConfig":
        """Create UIConfig from dictionary."""
        theme = data.get("theme", {})
        layout = data.get("layout", {})
        return cls(
            primary_color=theme.get("primary_color", "#007ACC"),
            secondary_color=theme.get("secondary_color", "#2C2C2C"),
            font_family=theme.get("font_family", "Segoe UI"),
            sidebar_width=layout.get("sidebar_width", 250),
            toolbar_height=layout.get("toolbar_height", 40),
        )


@dataclass
class StorageConfig:
    """Storage configuration settings."""

    default_backend: str
    backends: Dict[str, Dict[str, str]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StorageConfig":
        """Create StorageConfig from dictionary."""
        return cls(
            default_backend=data.get("default_backend", "json"),
            backends=data.get("backends", {}),
        )


class Config:
    """Main configuration class for TaskFlow."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize Config.

        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        self.config_path = config_path or Path("config/development.yaml")
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)

        self.environment = config_data.get("environment", "development")
        self.ui = UIConfig.from_dict(config_data.get("ui", {}))
        self.storage = StorageConfig.from_dict(config_data.get("storage", {}))
        self.logging = config_data.get("logging", {})
