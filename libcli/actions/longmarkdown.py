"""Print help for all commands in markdown."""

import argparse
from typing import Any, Sequence

from libcli.actions.basehelp import BaseHelpAction

__all__ = ["LongMarkdownHelpAction"]


class LongMarkdownHelpAction(BaseHelpAction):
    """Print help for all commands in markdown."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        _values: str | Sequence[Any] | None,
        _option_string: str | None = None,
    ) -> None:
        """Print help for all commands in markdown."""

        def _print_help(parser: argparse.ArgumentParser, atx: str) -> None:
            print(atx, parser.prog)
            print("```\n" + parser.format_help().rstrip() + "\n```\n")

        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        _print_help(parser, "#")

        if not parser._subparsers:
            parser.exit()

        for action in parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for subparser in action.choices.values():
                    subparser.formatter_class = argparse.RawDescriptionHelpFormatter
                    _print_help(subparser, "##")

        parser.exit()
