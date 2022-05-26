"""Print `Project-URL` and exit."""

import argparse
import contextlib
import importlib.metadata

from libcli.actions.base import BaseAction
from libcli.options.base import BaseOption


class PrintUrlOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print `Project-URL` and exit."""

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """Print `Project-URL` and exit."""

        parser.add_argument(
            "--print-url",
            action=PrintUrlAction,
            help="print project url and exit",
        )


class PrintUrlAction(BaseAction):
    """Print `Project-URL` and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print `Project-URL` and exit."""

        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            # https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use
            distro = importlib.metadata.distribution(namespace.cli.distname)
            print(distro.metadata.get("Project-URL", ""))

        parser.exit()
