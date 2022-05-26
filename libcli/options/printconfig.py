"""Print effective config and exit."""

import argparse
from pprint import pformat

from libcli.actions.base import BaseAction
from libcli.options.base import BaseOption


class PrintConfigOption(BaseOption):
    # pylint: disable=too-few-public-methods
    """Print effective config and exit."""

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """Print effective config and exit."""

        parser.add_argument(
            "--print-config",
            action=PrintConfigAction,
            help="print effective config and exit",
        )


class PrintConfigAction(BaseAction):
    """Print effective config and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print effective config and exit."""

        config = {}
        for name, value in namespace.cli.config.items():
            if name not in namespace.cli.exclude_print_config:
                optname = name.replace("-", "_")
                value = getattr(namespace, optname, value)
                config[name] = value if isinstance(value, (int, str)) else str(value)

        if (name := namespace.cli.config.get("config-name")) is not None:
            config = {name: config}

        print(pformat(config))
        parser.exit()
