"""Environment variable mixin for BaseCLI."""

from __future__ import annotations

import argparse
import os
from typing import Any

__all__ = ["EnvMixin"]


class EnvMixin:
    """Handles environment variable defaults for CLI options."""

    parser: argparse.ArgumentParser
    config: dict[Any, Any]

    @property
    def env_prefix(self) -> str:
        """Return the environment variable prefix.

        Derived from config `env-prefix`, `config-name`, or prog name.
        Converted to uppercase with hyphens replaced by underscores.
        """
        prefix: str | None = self.config.get("env-prefix") or self.config.get("config-name")
        if not prefix:
            parser = getattr(self, "parser", None)
            prefix = parser.prog if parser else "APP"
        return prefix.upper().replace("-", "_")

    def env_default(
        self,
        name: str,
        default: Any = None,
        type_: type | None = None,
    ) -> Any:
        """Get default value from environment variable.

        Checks for `{ENV_PREFIX}_{NAME}` environment variable.
        If found, converts to specified type. Otherwise returns default.

        Args:
            name: Option name (e.g., "verbose", "debug"). Will be uppercased.
            default: Default value if env var not set.
            type_: Type to convert env var value to (e.g., int, bool).
                   If None, returns string value or default's type.

        Returns:
            Environment variable value converted to type, or default.

        Example:
            >>> # With MYAPP_VERBOSE=2 in environment
            >>> self.env_default("verbose", 0, int)
            2
            >>> # With MYAPP_DEBUG=true in environment
            >>> self.env_default("debug", False, bool)
            True
        """
        env_name = f"{self.env_prefix}_{name.upper().replace('-', '_')}"
        env_value = os.environ.get(env_name)

        if env_value is None:
            return default

        if type_ is None:
            if default is not None:
                type_ = type(default)
            else:
                return env_value

        if type_ is bool:
            return env_value.lower() in ("1", "true", "yes", "on")

        return type_(env_value)
