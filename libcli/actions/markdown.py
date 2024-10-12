"""Print help in markdown."""

import argparse
from typing import Any, Sequence

from libcli.actions.basehelp import BaseHelpAction
from libcli.formatters.markdown import MarkdownHelpFormatter

__all__ = ["MarkdownHelpAction"]


class MarkdownHelpAction(BaseHelpAction):
    """Print help in markdown."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        _values: str | Sequence[Any] | None,
        _option_string: str | None = None,
    ) -> None:
        """Print help in markdown."""

        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()
