"""Render help in `markdown` format."""

import argparse
import re
from pathlib import Path
from typing import Any, Iterable

import tomli

__all__ = ["MarkdownHelpFormatter"]


class MarkdownHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Render help in `markdown` format."""

    # @classmethod
    # def _md_code(cls, raw_text, language=None):
    #     return (
    #         f"```{language or ''}\n"
    #         + cls._md_escape(raw_text.rstrip(), characters="`")
    #         + "\n```\n\n"
    #     )

    # @staticmethod
    # def _md_escape(raw_text, characters="*_"):
    #     def _escape_char(match):
    #         return "\\%s" % match.group(0)
    #     pattern = "[%s]" % re.escape(characters)
    #     return re.sub(pattern, _escape_char, raw_text)

    @staticmethod
    def _md_heading(text: str | None, level: int) -> str:
        level = min(max(level, 0), 6)
        _text = str(text) if text else ""
        return str("#" * level + " " + _text) if level else _text

    # def md_inline_code(raw_text):
    #     return "`%s`" % _md_escape(raw_text, characters="`")
    #
    # def md_bold(raw_text):
    #     return "**%s**" % _md_escape(raw_text, characters="*")
    #
    # def md_italic(raw_text):
    #     return "*%s*" % _md_escape(raw_text, characters="*")
    #
    # def md_link(link_text, link_target):
    #     return "[%s](%s)" % (
    #         _md_escape(link_text, characters="]"),
    #         _md_escape(link_target, characters=")"),
    #     )

    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ):
        """Initialize MarkdownHelpFormatter."""
        self._md_level = {
            "title": 3,  # 1 and 2 render <hr/> on github
            "heading": 4,
        }

        super().__init__(prog, indent_increment, max_help_position, width)

        self._md_title = self._prog
        path = Path("pyproject.toml")
        if (
            path.exists()
            and (config := tomli.loads(path.read_text(encoding="utf-8")))
            and (project := config.get("project"))
            and (description := project.get("description"))
        ):
            self._md_title += " - " + description

    def _format_usage(
        self,
        usage: str | None,
        actions: Iterable[argparse.Action],
        groups: Any,
        prefix: str | None,
    ) -> str:

        usage_text = super()._format_usage(usage, actions, groups, prefix)

        lines = usage_text.splitlines(keepends=True)

        # Replace 1st len("usage: ") chars with 4 spaces on all lines.
        if usage_text.startswith("usage: "):
            lines = [x[7:] for x in lines]
        lines = [" " * 4 + x for x in lines]

        return (
            "\n"
            + self._md_heading("Usage", level=self._md_level["heading"])
            + "\n"
            + "".join(lines)
            + "\n"
        )

    def format_help(self) -> str:
        """Format help."""
        self._root_section.heading = self._md_heading(
            self._md_title, level=self._md_level["title"]
        )
        return super().format_help()

    def start_section(self, heading: str | None) -> None:
        """Start section."""
        if heading and (
            heading.startswith("options") or heading.startswith("positional arguments")
        ):
            heading = heading.title()
        super().start_section(self._md_heading(heading, level=self._md_level["heading"]))

    def _format_action(self, action: argparse.Action) -> str:
        # indent at least 4 for code block
        _save_indent = self._current_indent
        self._current_indent = max(4, min(4, self._current_indent))
        action_help = super()._format_action(action)
        self._current_indent = _save_indent
        return action_help

    class _Section(argparse.HelpFormatter._Section):
        # pylint: disable=protected-access
        # pylint: disable=too-few-public-methods
        def format_help(self) -> str:
            # remove trailing colon from header line
            section_text = super().format_help()
            section_text = re.sub(r"^(\s*#+ [^\n]+):\n", "\\1\n", section_text)
            return section_text
