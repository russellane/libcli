"""Print help in markdown."""

from libcli.actions.basehelp import BaseHelpAction
from libcli.formatters.markdown import MarkdownHelpFormatter


class MarkdownHelpAction(BaseHelpAction):
    """Print help in markdown."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print help in markdown."""

        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()
