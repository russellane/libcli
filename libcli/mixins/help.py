"""Help text utilities mixin for BaseCLI."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from libcli.formatters.color import ColorHelpFormatter

__all__ = ["HelpMixin"]

# pylint: disable=protected-access


class HelpMixin:  # pylint: disable=too-few-public-methods
    """Handles help text normalization and formatting."""

    parser: argparse.ArgumentParser
    help_first_char: str
    help_line_ending: str

    def add_default_to_help(
        self,
        arg: argparse.Action,
        parser: argparse.ArgumentParser | argparse._ArgumentGroup | None = None,
    ) -> None:
        """Add default value to help text for `arg` in `parser`."""

        if parser is None:
            parser = self.parser
        default = parser.get_default(arg.dest)
        if default is None:
            return
        if isinstance(arg.const, bool) and not arg.const:
            default = not default
        else:
            default = str(default)
            home = str(Path.home())
            if default.startswith(home):
                default = "~" + default[len(home) :]
        default = f" (default: `{default}`)"

        if arg.help and arg.help.endswith(self.help_line_ending):
            arg.help = arg.help[: -len(self.help_line_ending)] + default + self.help_line_ending
        else:
            arg.help = (arg.help or "") + default

    def _normalize_help_text(self, text: str | None) -> str | None:
        """Return help `text` with normalized first-character and line-ending."""

        if text and text != argparse.SUPPRESS:
            if self.help_line_ending and not text.endswith(self.help_line_ending):
                text += self.help_line_ending
            if self.help_first_char == "upper":
                text = text[0].upper() + text[1:]
            elif self.help_first_char == "lower":
                text = text[0].lower() + text[1:]
        return text

    def _finalize(self) -> None:
        """Normalize `formatter_class` and `help` text of all parsers."""

        if os.getenv("NOCOLOR"):
            formatter_class = argparse.RawDescriptionHelpFormatter
        else:
            formatter_class = ColorHelpFormatter

        if self.parser.formatter_class == argparse.HelpFormatter:
            self.parser.formatter_class = formatter_class

        for action in self.parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                for choice in action._choices_actions:
                    choice.help = self._normalize_help_text(choice.help)
                for subparser in action.choices.values():
                    if subparser.formatter_class == argparse.HelpFormatter:
                        subparser.formatter_class = formatter_class
                    if subparser._actions:
                        for subact in subparser._actions:
                            subact.help = self._normalize_help_text(subact.help)
            else:
                action.help = self._normalize_help_text(action.help)
