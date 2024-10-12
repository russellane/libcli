"""Modified `PdmFormatter` from `pdm/pdm/cli/utils.py`."""

import argparse
import functools
import re
from typing import Iterable

from colors.colors import color as _color  # type: ignore

__all__ = ["ColorHelpFormatter"]

_color_code_span = functools.partial(_color, fg="yellow")
_color_header = functools.partial(_color, fg="cyan")
_color_title = functools.partial(_color, fg="yellow", style="bold")
_color_usage = functools.partial(_color, fg="yellow", style="bold")

_RE_CODE_SPAN = None


def _colorize_text(text: str) -> str:
    global _RE_CODE_SPAN  # noqa
    if _RE_CODE_SPAN is None:
        _RE_CODE_SPAN = re.compile(r"`([^`]*)`")
    return _RE_CODE_SPAN.sub(_color_code_span(r"`\1`"), text)


class ColorHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Colorize help."""

    def start_section(self, heading: str | None) -> None:
        """Colorize start of help section."""

        return super().start_section(_color_title(heading.title()) if heading else heading)

    def _format_usage(
        self,
        usage: str | None,
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._MutuallyExclusiveGroup],
        prefix: str | None,
    ) -> str:
        if prefix is None:
            prefix = "Usage: "
        result = super()._format_usage(usage, actions, groups, prefix)
        if prefix:
            return result.replace(prefix, _color_usage(prefix))
        return result  # pragma: no cover

    def _format_action(self, action: argparse.Action) -> str:
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup  # noqa: f-string

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, "", action_width, action_header  # type: ignore
            action_header = "%*s%-*s  " % tup  # type: ignore  # noqa: f-string
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup  # noqa: f-string
            indent_first = help_position

        # collect the pieces of the action help
        parts = [_color_header(action_header)]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_text = _colorize_text(help_text)
            help_lines = self._split_lines(help_text, help_width)
            parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))  # noqa: f-string
            for line in help_lines[1:]:
                parts.append("%*s%s\n" % (help_position, "", line))  # noqa: f-string

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith("\n"):
            parts.append("\n")  # pragma: no cover

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

    def add_text(self, text: str | None) -> None:
        """Colorize and add `text` to section."""
        if text:
            text = _colorize_text(text)
        super().add_text(text)

    def _format_text(self, text: str) -> str:
        return _colorize_text(super()._format_text(text))
