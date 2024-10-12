"""Print `Project-URL` and exit."""

import argparse
import contextlib
import importlib.metadata
from typing import Any

from libcli.actions.basehelp import BaseHelpAction
from libcli.options.base import BaseOption

__all__ = ["PrintUrlOption"]


class PrintUrlOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print `Project-URL` and exit."""

    def __init__(self, parser: argparse.ArgumentParser | argparse._ArgumentGroup) -> None:
        """Print `Project-URL` and exit."""

        parser.add_argument(
            "--print-url",
            action=PrintUrlAction,
            help="print project url and exit",
        )


class PrintUrlAction(BaseHelpAction):
    """Print `Project-URL` and exit."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        _values: Any,
        _option_string: Any = None,
    ) -> None:
        """Print `Project-URL` and exit."""

        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            # https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use
            distro = importlib.metadata.distribution(namespace.cli.distname)
            if distro is not None and distro.metadata is not None:
                print(distro.metadata.json.get("Project-URL", ""))

        parser.exit()
