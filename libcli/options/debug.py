"""Print diagnostics and exit."""

import argparse
from pprint import pformat
from typing import Any

from libcli.actions.basehelp import BaseHelpAction
from libcli.options.base import BaseOption

__all__ = ["DebugOption"]


class DebugOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print diagnostics and exit."""

    def __init__(self, parser: argparse.ArgumentParser | argparse._ArgumentGroup) -> None:
        """Print diagnostics and exit."""

        parser.add_argument(
            "-X",
            action=DebugAction,
            help=argparse.SUPPRESS,
        )


class DebugAction(BaseHelpAction):
    """Print diagnostics and exit."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        _values: Any,
        _option_string: Any | None = None,
    ) -> None:
        """Print diagnostics and exit."""

        if "ic" in globals():
            ic(namespace.cli.__dict__)  # type: ignore # noqa
            ic(parser.__dict__)  # type: ignore # noqa
            ic(namespace)  # type: ignore # noqa
        else:
            print(pformat(namespace.cli.__dict__))
            print(pformat(parser.__dict__))
            print(pformat(namespace))

        parser.exit()
