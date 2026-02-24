"""Print effective config and exit."""

import argparse
from typing import Any

import tomli_w

from libcli.actions.basehelp import BaseHelpAction
from libcli.options.base import BaseOption

__all__ = ["PrintConfigOption"]


class PrintConfigOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print effective config and exit."""

    def __init__(self, parser: argparse.ArgumentParser | argparse._ArgumentGroup) -> None:
        """Print effective config and exit."""

        parser.add_argument(
            "--print-config",
            action=PrintConfigAction,
            help="print effective config and exit",
        )


class PrintConfigAction(BaseHelpAction):
    """Print effective config and exit."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        _values: Any,
        _option_string: Any | None = None,
    ) -> None:
        """Print effective config and exit."""

        config: dict[str, Any] = {}
        for name, cfg_value in namespace.cli.config.items():
            if name not in namespace.cli.exclude_print_config:
                optname = name.replace("-", "_")
                value = getattr(namespace, optname, cfg_value)
                config[name] = self._toml_value(value)

        if (name := namespace.cli.config.get("config-name")) is not None:
            config = {name: config}

        print(tomli_w.dumps(config))
        parser.exit()

    @staticmethod
    def _toml_value(value: Any) -> Any:
        """Convert value to TOML-compatible type."""
        if isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, list):
            return [PrintConfigAction._toml_value(v) for v in value]
        if isinstance(value, dict):
            return {k: PrintConfigAction._toml_value(v) for k, v in value.items()}
        # Convert Path and other types to string
        return str(value)
