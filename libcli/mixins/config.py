"""Configuration mixin for BaseCLI."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import tomli

from libcli.exceptions import ConfigFileNotFoundError

__all__ = ["ConfigMixin"]


class ConfigMixin:  # pylint: disable=too-few-public-methods
    """Handles config file loading and management."""

    config: dict[Any, Any]
    exclude_print_config: list[str]
    options: argparse.Namespace
    argv: list[str] | None
    _config_error: ConfigFileNotFoundError | None = None

    def init_config(self) -> None:
        """Parse command line to load contents of `--config FILE` only.

        Reads `--config FILE` if given, else `self.config["config-file"]`
        if present, making the effective configuration available to
        building the ArgumentParser, add_argument, set_defaults, etc.
        """

        base_config = {
            # name of config file
            # optional: adds `--config FILE` option when set.
            # regardless: `--print-config` will be added.
            "config-file": None,
            # toml [section-name]
            # optional:
            # encouraged:
            # regardless: of `config-file`.
            "config-name": None,
            # distribution name, not importable package name
            "dist-name": None,
            # --verbose
            "verbose": 0,
        }

        # merge any missing base items into user items.
        if self.config:
            base_config.update(self.config)
        self.config = base_config

        # don't `--print-config` any of the base items or user excludes.
        for key in base_config:
            if key not in self.exclude_print_config:
                self.exclude_print_config.append(key)

        self._update_config_from_file()

    def _update_config_from_file(self) -> None:

        # sneak a peak for `--verbose` and `--config FILE`.
        parser = argparse.ArgumentParser(add_help=False)
        self._add_verbose_option(parser)  # type: ignore[attr-defined]
        self._add_config_option(parser)  # type: ignore[attr-defined]
        self.options, _ = parser.parse_known_args(self.argv)

        self.init_logging(self.options.verbose)  # type: ignore[attr-defined]

        if not self.options.config_file:
            self.debug("config-file not defined or given.")  # type: ignore[attr-defined]
            return

        self.debug(  # type: ignore[attr-defined]
            f"reading config-file `{self.options.config_file}`."
        )

        try:
            _path = Path(self.options.config_file).expanduser()
            _text = _path.read_text(encoding="utf-8")
            config = tomli.loads(_text)
        except FileNotFoundError:
            if self.options.config_file != self.config["config-file"]:
                # postpone calling `parser.error` to full parser.
                self._config_error = ConfigFileNotFoundError(str(self.options.config_file))
            else:
                self.debug(  # type: ignore[attr-defined]
                    f"config file not found: {self.options.config_file}; ignoring."
                )
            return

        if (section := self.config.get("config-name")) is not None:
            config = config.get(section, config)

        for name, value in config.items():
            if name in self.config:
                _type = type(self.config[name])
                config[name] = _type(value)

        self.config.update(config)

    def _update_config_from_options(self, options: object) -> None:

        for name, value in self.config.items():
            if name not in self.exclude_print_config:
                optname = name.replace("-", "_")
                self.config[name] = getattr(options, optname, value)
