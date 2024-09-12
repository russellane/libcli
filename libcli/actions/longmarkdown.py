"""Print help for all commands in markdown."""

import argparse

from libcli.actions.basehelp import BaseHelpAction


class LongMarkdownHelpAction(BaseHelpAction):
    """Print help for all commands in markdown."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values,
        option_string=None,
    ) -> None:
        """Print help for all commands in markdown."""

        def _print_help(parser, atx: str) -> None:
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
