"""Command line interface base module."""

import argparse
import contextlib
import importlib
import importlib.metadata
import logging
import os
import pkgutil
import sys
import textwrap
from pathlib import Path
from typing import Callable, List, Optional

import argcomplete
import tomli
from colors.colors import color

with contextlib.suppress(ImportError):
    from loguru import logger  # noqa

with contextlib.suppress(ImportError):
    import icecream  # noqa
    from icecream import ic  # noqa

    icecream.install()
    icecream.ic.configureOutput(prefix="=====>\n", includeContext=True)

from libcli.actions.basehelp import BaseHelpAction
from libcli.actions.longhelp import LongHelpAction
from libcli.actions.longmarkdown import LongMarkdownHelpAction
from libcli.actions.markdown import MarkdownHelpAction
from libcli.formatters.color import ColorHelpFormatter
from libcli.options.debug import DebugOption
from libcli.options.printconfig import PrintConfigOption
from libcli.options.printurl import PrintUrlOption

# pylint: disable=protected-access


class BaseCLI:
    """Command line interface base class."""

    argv: [str] = []
    config: dict = {}
    exclude_print_config: [str] = []
    parser: argparse.ArgumentParser = None
    options: argparse.Namespace = None
    add_parser: Callable = None
    help_first_char = "upper"
    help_line_ending = "."
    init_logging_called = False

    def __init__(self, argv: Optional[List[str]] = None) -> None:
        """Build and parse command line.

        Args:
            argv:       command line argument list.

        Attributes:
            argv:       command line argument list of strings.
            config:     configuration dict.
            exclude_print_config: list of keys to not write to config-file.
            parser:     argument parser.
            options:    parsed arguments; from `self.parser.parse_args(argv)`.
        """

        self.argv = argv
        self.init_config()
        self.init_parser()
        self.set_defaults()
        self.add_arguments()
        self._add_common_options(self.parser)
        self._finalize()
        argcomplete.autocomplete(self.parser)
        self.options = self._parse_args()

    def init_config(self) -> None:
        """Parse command line to load contents of `--config FILE` only.

        Reads `--config FILE` if given, else `self.config["config-file"]`
        if present, making the effective configuration available to
        building the ArgumentParser, add_argument, set_defaults, etc.
        """

        base_config = {
            # name of config file
            # optional: adds `--config FILE` option when set.
            # regardless: `--print-config` will be added.
            "config-file": None,
            # toml [section-name]
            # optional:
            # encouraged:
            # regardless: of `config-file`.
            "config-name": None,
            # distribution name, not importable package name
            "dist-name": None,
            # --verbose
            "verbose": 0,
        }

        # merge any missing base items into user items.
        if self.config:
            base_config.update(self.config)
        self.config = base_config

        # don't `--print-config` any of the base items or user excludes.
        for key in base_config:
            if key not in self.exclude_print_config:
                self.exclude_print_config.append(key)

        self._update_config_from_file()

    def init_logging(self, verbose: int) -> None:
        """Set logging levels based on `--verbose`."""

        if not self.init_logging_called:
            self.__class__.init_logging_called = True

            # stdlib:
            #    (dflt)           -v            -vv
            _ = [logging.WARNING, logging.INFO, logging.DEBUG]
            logging.basicConfig(level=_[min(verbose, len(_) - 1)])

            if "logger" in globals():
                # loguru:
                #    (dflt)  -v       -vv
                _ = ["INFO", "DEBUG", "TRACE"]
                level = _[min(verbose, len(_) - 1)]
                logger.remove()
                logger.add(sys.stderr, level=level)

    def init_parser(self) -> None:
        """Implement in subclass, if desired."""
        self.ArgumentParser()

    def set_defaults(self) -> None:
        """Implement in subclass, if desired."""

    def add_arguments(self) -> None:
        """Implement in subclass, probably desired."""

    def ArgumentParser(self, **kwargs) -> argparse.ArgumentParser:  # noqa: snake-case
        """Initialize `self.parser`."""

        kwargs["add_help"] = False
        self.parser = argparse.ArgumentParser(**kwargs)
        self.parser.set_defaults(cli=self)
        return self.parser

    def add_subcommand_classes(self, subcommand_classes) -> None:
        """Add list of subcommands to this parser."""

        # https://docs.python.org/3/library/argparse.html#sub-commands
        self.init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)
        for subcommand_class in subcommand_classes:
            subcommand_class(self)

        # equiv to module: .commands.help import Command as HelpCommand
        # sub = self.add_subcommand_parser("help", help="same as `--help`")
        # sub.set_defaults(cmd=self.parser.print_help)

    def add_subcommand_modules(
        self,
        modname: str,
        prefix: str = None,
        suffix: str = None,
    ) -> None:
        """Add all subcommands in module `modname`.

        e.g., cli.add_subcommand_modules("wumpus.commands")
        or,   cli.add_subcommand_modules("wumpus.cli.commands")
        or wherever your command modules are.

        1. Load each module in containing module `modname`,
        2. Instantiate an instance each module's `Command` class, and
        3. Add the command to this cli.

        If all command classes are not named `Command`, then they must all
        begin and/or end with common tags. Pass `prefix` and/or `suffix` to
        specify, and the longest matching class will be used. Multiple
        command classes could be defined in one module this way.

        e.g.,
            wumpus/commands/move.py
                class WumpusMoveCmd(BaseCmd):
                    ...

            wumpus/commands/shoot.py
                class WumpusCmd(BaseCmd):
                    ...
                class WumpusShootCmd(WumpusCmd)
                    ...

            cli.add_subcommand_modules("wumpus.commands", prefix="Wumpus", suffix="Cmd")
        """

        self.init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)

        commands_module_path = importlib.import_module(modname, __name__).__path__
        base_name = (prefix or "") + (suffix or "")

        for modinfo in pkgutil.iter_modules(commands_module_path):
            module = importlib.import_module(f"{modname}.{modinfo.name}", __name__)

            if not prefix and not suffix and hasattr(module, "Command"):
                module.Command(self)
                continue

            for name in [x for x in dir(module) if x != base_name]:
                if prefix and not name.startswith(prefix):
                    continue
                if suffix and not name.endswith(suffix):
                    continue
                try:
                    cmd_class = getattr(module, name)
                except AttributeError:
                    continue
                cmd_class(self)

    def init_subcommands(self, **kwargs):
        """Prepare to add subcommands to main parser."""

        subparsers = self.parser.add_subparsers(**kwargs)
        self.add_parser = subparsers.add_parser

    def add_default_to_help(
        self,
        arg: argparse.Action,
        parser: argparse.ArgumentParser = None,
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

        if arg.help.endswith(self.help_line_ending):
            arg.help = arg.help[: -len(self.help_line_ending)] + default + self.help_line_ending
        else:
            arg.help += default

    def normalize_help_text(self, text: str) -> str:
        """Return help `text` with normalized first-character and line-ending."""

        if text and text != argparse.SUPPRESS:
            if self.help_line_ending and not text.endswith(self.help_line_ending):
                text += self.help_line_ending
            if self.help_first_char == "upper":
                text = text[0].upper() + text[1:]
            elif self.help_first_char == "lower":
                text = text[0].lower() + text[1:]
        return text

    @staticmethod
    def dedent(text: str) -> str:
        """Make `textwrap.dedent` convenient."""
        return textwrap.dedent(text).strip()

    def error(self, text: str) -> None:
        """Print an ERROR message to `stdout`."""
        _ = self  # unused; avoiding @staticmethod
        print(color("ERROR: " + text, "red"))

    def info(self, text: str) -> None:
        """Print an INFO message to `stdout`."""
        if self.options.verbose > 0:
            print(color("INFO: " + text, "cyan"))

    def debug(self, text: str) -> None:
        """Print a DEBUG message to `stdout`."""
        if self.options.verbose > 1:
            print(color("DEBUG: " + text, "white"))

    # public
    # -------------------------------------------------------------------------------
    # private

    def _update_config_from_file(self) -> None:

        # sneak a peak for `--verbose` and `--config FILE`.
        parser = argparse.ArgumentParser(add_help=False)
        self._add_verbose_option(parser)
        self._add_config_option(parser)
        self.options, _ = parser.parse_known_args(self.argv)

        self.init_logging(self.options.verbose)

        if not self.options.config_file:
            self.debug("config-file not defined or given.")
            return

        self.debug(f"reading config-file `{self.options.config_file}`.")

        try:
            config = tomli.loads(self.options.config_file.read_text())
        except FileNotFoundError as err:
            if self.options.config_file != self.config["config-file"]:
                # postpone calling `parser.error` to full parser.
                self.config["config-file"] = err
            else:
                self.debug(f"{err}; ignoring.")
            return

        if (section := self.config.get("config-name")) is not None:
            config = config.get(section, config)

        for name, value in config.items():
            if name in self.config:
                _type = type(self.config[name])
                config[name] = _type(value)

        self.config.update(config)

    def _add_common_options(self, parser: argparse.ArgumentParser) -> None:
        """Add common options to given `parser`."""

        group = parser.add_argument_group("General options")

        DebugOption(group)

        group.add_argument(
            "-h",
            "--help",
            action=BaseHelpAction,
            help="show this help message and exit",
        )

        if self.add_parser:
            group.add_argument(
                "-H",
                "--long-help",
                action=LongHelpAction,
                help="show help for all commands and exit",
            )

        group.add_argument(
            "--md-help",
            action=LongMarkdownHelpAction if self.add_parser else MarkdownHelpAction,
            help=argparse.SUPPRESS,
            # help="show this help message in markdown format and exit",
        )

        self._add_verbose_option(group)
        self._add_version_option(group)

        if self.config.get("config-file"):
            self._add_config_option(group)

        PrintConfigOption(group)
        PrintUrlOption(group)

    @staticmethod
    def _add_verbose_option(parser: argparse.ArgumentParser) -> None:
        """Add `--verbose` to given `parser`."""

        parser.add_argument(
            "-v",
            "--verbose",
            default=0,
            action="count",
            help="`-v` for detailed output and `-vv` for more detailed",
        )

    def _add_version_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--version` to given `parser`."""

        version = "0.0.0"
        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            # https://docs.python.org/3/library/importlib.metadata.html#distribution-versions
            version = importlib.metadata.version(self.distname)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version,
            help="print version number and exit",
        )

    @property
    def distname(self) -> str:
        """Return `name` for `importlib.metadata` functions."""

        return self.config.get("dist-name") or self.config.get("config-name") or self.parser.prog

    def _add_config_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--config FILE` to given `parser`."""

        arg = parser.add_argument(
            "--config",
            dest="config_file",
            metavar="FILE",
            default=self.config.get("config-file"),
            type=Path,
            help="use config `FILE`",
        )
        self.add_default_to_help(arg, parser)

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
                    choice.help = self.normalize_help_text(choice.help)
                for subparser in action.choices.values():
                    if subparser.formatter_class == argparse.HelpFormatter:
                        subparser.formatter_class = formatter_class
                    if subparser._actions:
                        for subact in subparser._actions:
                            subact.help = self.normalize_help_text(subact.help)
            else:
                action.help = self.normalize_help_text(action.help)

    def _parse_args(self) -> argparse.Namespace:
        """Parse command line and return options."""

        options = self.parser.parse_args(self.argv)

        if isinstance(self.config.get("config-file"), Exception):
            # postponed from load_config
            self.parser.error(self.config["config-file"])

        self._update_config_from_options(options)
        return options

    def _update_config_from_options(self, options):

        for name, value in self.config.items():
            if name not in self.exclude_print_config:
                optname = name.replace("-", "_")
                self.config[name] = getattr(options, optname, value)
