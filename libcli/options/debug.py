"""Print diagnostics and exit."""

import argparse
from pprint import pformat

from libcli.actions.base import BaseAction
from libcli.options.base import BaseOption


class DebugOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print diagnostics and exit."""

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """Print diagnostics and exit."""

        parser.add_argument(
            "-X",
            action=DebugAction,
            help=argparse.SUPPRESS,
        )


class DebugAction(BaseAction):
    """Print diagnostics and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print diagnostics and exit."""

        if "ic" in globals():
            ic(namespace.cli.__dict__)  # noqa
            ic(parser.__dict__)  # noqa
            ic(namespace)  # noqa
        else:
            print(pformat(namespace.cli.__dict__))
            print(pformat(parser.__dict__))
            print(pformat(namespace))

        parser.exit()
