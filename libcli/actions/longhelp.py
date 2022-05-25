"""Print help for all commands."""

import argparse

from libcli.actions.basehelp import BaseHelpAction


class LongHelpAction(BaseHelpAction):
    """Print help for all commands."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print help for all commands."""

        def _print_help(parser) -> None:
            print(f" {parser.prog.upper()} ".center(80, "-") + "\n")
            print(parser.format_help())

        _print_help(parser)

        for action in parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for subparser in action.choices.values():
                    _print_help(subparser)

        parser.exit()


#   @staticmethod
#   def _see_also(parser) -> str:
#
#       # xylint: disable=protected-access
#       also = {}
#       for action in parser._subparsers._actions:
#           if isinstance(action, argparse._SubParsersAction):
#               for name in action.choices:
#                   also[name] = f"{parser.prog}-{name}"
#       if not also:
#           return ""
#
#       formatter = parser._get_formatter()
#       return "\n\nSee Also: \n" + textwrap.fill(
#           ", ".join(also.values()) + ".",
#           width=formatter._width,
#           initial_indent=" " * formatter._indent_increment,
#           subsequent_indent=" " * formatter._indent_increment,
#       )
