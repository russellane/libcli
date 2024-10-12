"""Print completion scripts for `SHELL` and exit."""

import argparse
import subprocess
from typing import Any, Sequence

from libcli.actions.base import BaseAction
from libcli.options.base import BaseOption

__all__ = ["CompletionOption"]


class CompletionOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print completion scripts for `SHELL` and exit."""

    def __init__(self, parser: argparse.ArgumentParser | argparse._ArgumentGroup) -> None:
        """Print completion scripts for `SHELL` and exit."""

        arg = parser.add_argument(
            "--completion",
            nargs="?",
            dest="shell",
            default="bash",
            action=CompletionAction,
            help="Print completion scripts for `SHELL` and exit",
        )
        parser.get_default("cli").add_default_to_help(arg, parser)


class CompletionAction(BaseAction):
    """Print completion scripts for `SHELL` and exit."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        _option_string: str | None = None,
    ) -> None:
        """Print completion scripts for `SHELL` and exit."""

        argv = [
            "register-python-argcomplete",
            "-s",
            values if values else namespace.shell,
            parser.prog,
        ]
        proc = subprocess.run(argv, check=False)
        parser.exit(proc.returncode)
