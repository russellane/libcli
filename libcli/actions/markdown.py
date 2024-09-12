"""Print help in markdown."""

import argparse

from libcli.actions.basehelp import BaseHelpAction
from libcli.formatters.markdown import MarkdownHelpFormatter


class MarkdownHelpAction(BaseHelpAction):
    """Print help in markdown."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values,
        option_string=None,
    ) -> None:
        """Print help in markdown."""

        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()
