"""Common options mixin for BaseCLI."""

from __future__ import annotations

import argparse
import contextlib
import importlib.metadata
from pathlib import Path
from typing import Any, Callable

from libcli.actions.basehelp import BaseHelpAction
from libcli.actions.longhelp import LongHelpAction
from libcli.actions.longmarkdown import LongMarkdownHelpAction
from libcli.actions.markdown import MarkdownHelpAction
from libcli.options.completion import CompletionOption
from libcli.options.printconfig import PrintConfigOption
from libcli.options.printurl import PrintUrlOption

__all__ = ["OptionsMixin"]


class OptionsMixin:  # pylint: disable=too-few-public-methods
    """Handles common CLI options (help, version, verbose, config, etc.)."""

    parser: argparse.ArgumentParser
    config: dict[Any, Any]
    add_parser: Callable[[Any], argparse.ArgumentParser] | None

    def _add_common_options(self, parser: argparse.ArgumentParser) -> None:
        """Add common options to given `parser`."""

        group = parser.add_argument_group("General options")

        group.add_argument(
            "-h",
            "--help",
            action=BaseHelpAction,
            help="show this help message and exit",
        )

        if self.add_parser:
            group.add_argument(
                "-H",
                "--long-help",
                action=LongHelpAction,
                help="show help for all commands and exit",
            )

        group.add_argument(
            "--md-help",
            action=LongMarkdownHelpAction if self.add_parser else MarkdownHelpAction,
            help=argparse.SUPPRESS,
            # help="show this help message in markdown format and exit",
        )

        self._add_verbose_option(group)
        self._add_version_option(group)

        if self.config.get("config-file"):
            self._add_config_option(group)

        PrintConfigOption(group)
        PrintUrlOption(group)
        CompletionOption(group)

    @staticmethod
    def _add_verbose_option(
        parser: argparse.ArgumentParser | argparse._ArgumentGroup,
    ) -> None:
        """Add `--verbose` to given `parser`."""

        parser.add_argument(
            "-v",
            "--verbose",
            default=0,
            action="count",
            help="`-v` for detailed output and `-vv` for more detailed",
        )

    def _add_version_option(
        self,
        parser: argparse.ArgumentParser | argparse._ArgumentGroup,
    ) -> None:
        """Add `--version` to given `parser`."""

        version = "0.0.0"
        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            # https://docs.python.org/3/library/importlib.metadata.html#distribution-versions
            version = importlib.metadata.version(self.distname)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version,
            help="print version number and exit",
        )

    @property
    def distname(self) -> str:
        """Return `name` for `importlib.metadata` functions."""

        return self.config.get("dist-name") or self.config.get("config-name") or self.parser.prog

    def _add_config_option(
        self,
        parser: argparse.ArgumentParser | argparse._ArgumentGroup,
    ) -> None:
        """Add `--config FILE` to given `parser`."""

        arg = parser.add_argument(
            "--config",
            dest="config_file",
            metavar="FILE",
            default=self.config.get("config-file"),
            type=Path,
            help="use config `FILE`",
        )
        self.add_default_to_help(arg, parser)  # type: ignore[attr-defined]
