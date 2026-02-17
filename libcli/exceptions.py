"""Custom exceptions for libcli."""

__all__ = ["ConfigError", "ConfigFileNotFoundError"]


class ConfigError(Exception):
    """Base exception for configuration errors."""


class ConfigFileNotFoundError(ConfigError):
    """Raised when a specified config file is not found."""

    def __init__(self, path: str) -> None:
        """Initialize with the path that was not found."""
        self.path = path
        super().__init__(f"config file not found: {path}")
