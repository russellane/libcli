"""Command line interface base module.

This module provides the `BaseCLI` class.
"""

import argparse
import contextlib
from typing import Any, Callable

import argcomplete
from colors.colors import color  # type: ignore

with contextlib.suppress(ImportError):
    import icecream  # type: ignore
    from icecream import ic  # noqa

    icecream.install()
    icecream.ic.configureOutput(prefix="=====>\n", includeContext=True)

from libcli.helpers import dedent, hideuser
from libcli.mixins.config import ConfigMixin
from libcli.mixins.env import EnvMixin
from libcli.mixins.help import HelpMixin
from libcli.mixins.logging import LoggingMixin
from libcli.mixins.options import OptionsMixin
from libcli.mixins.subcommands import SubcommandMixin

__all__ = ["BaseCLI"]


class BaseCLI(ConfigMixin, EnvMixin, LoggingMixin, OptionsMixin, SubcommandMixin, HelpMixin):
    """Command line interface base class.

    $ cat minimal.py

        from libcli import BaseCLI
        class HelloCLI(BaseCLI):
            def main(self) -> None:
                print("Hello")
        if __name__ == "__main__":
            HelloCLI().main()

    $ python minimal.py -h

        Usage: minimal.py [-h] [-v] [-V] [--print-config] [--print-url] [--completion [SHELL]]

        General Options:
          -h, --help            Show this help message and exit.
          -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
          -V, --version         Print version number and exit.
          --print-config        Print effective config and exit.
          --print-url           Print project url and exit.
          --completion [SHELL]  Print completion scripts for `SHELL` and exit (default: `bash`).

    $ cat simple.py

        from libcli import BaseCLI

        class HelloCLI(BaseCLI):

            def init_parser(self) -> None:
                self.parser = self.ArgumentParser(
                    prog=__package__,
                    description="This program says hello.",
                )

            def add_arguments(self) -> None:
                self.parser.add_argument(
                    "--spanish",
                    action="store_true",
                    help="Say hello in Spanish.",
                )
                self.parser.add_argument(
                    "name",
                    help="The person to say hello to.",
                )

            def main(self) -> None:
                if self.options.spanish:
                    print(f"Hola, {self.options.name}!")
                else:
                    print(f"Hello, {self.options.name}!")

        if __name__ == "__main__":
            HelloCLI().main()

    $ python simply.py -h

        Usage: simple.py [--spanish] [-h] [-v] [-V] [--print-config] [--print-url]
                         [--completion [SHELL]] name

        This program says hello.

        Positional Arguments:
          name                  The person to say hello to.

        Options:
          --spanish             Say hello in Spanish.

        General Options:
          -h, --help            Show this help message and exit.
          -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
          -V, --version         Print version number and exit.
          --print-config        Print effective config and exit.
          --print-url           Print project url and exit.
          --completion [SHELL]  Print completion scripts for `SHELL` and exit (default: `bash`).

    """

    argv: list[str] | None = []
    config: dict[Any, Any] = {}
    exclude_print_config: list[str] = []
    parser: argparse.ArgumentParser
    options: argparse.Namespace
    add_parser: Callable[[Any], argparse.ArgumentParser] | None = None
    help_first_char = "upper"
    help_line_ending = "."

    # Static method wrappers for backwards compatibility
    dedent = staticmethod(dedent)
    hideuser = staticmethod(hideuser)

    def __init__(self, argv: list[str] | None = None) -> None:
        """Build and parse command line.

        After setting `self.argv`, the constructor calls these public methods,
        which the subclass MAY implement, in order:

            init_config:
            init_logging:
            init_parser: should call `self.ArgumentParser`.
            set_defaults:
            add_arguments: should call `self.parser.add_argument`
                           or `self.add_subcommand_classes`.

        Args:
            argv:       command line argument list.

        Attributes:
            argv:       command line argument list of strings.
            config:     configuration dict.
            exclude_print_config: list of keys to not write to config-file.
            parser:     argument parser.
            options:    parsed arguments; from `self.parser.parse_args(argv)`.
            help_first_char: "upper" | "lower"; defines how to normalize
                        the first character of all help strings.
            help_line_ending: "."; defines how to normalize the last character
                        of all help strings.
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

    def init_parser(self) -> None:
        """Implement in subclass, if desired."""
        self.ArgumentParser()

    def set_defaults(self) -> None:
        """Implement in subclass, if desired."""

    def add_arguments(self) -> None:
        """Implement in subclass, probably desired."""

    def ArgumentParser(  # noqa: N802  pylint: disable=invalid-name
        self, **kwargs: str
    ) -> argparse.ArgumentParser:
        """Wrap and return results from `argparse.ArgumentParser`.

        Args:
            kwargs: passed through to `argparse.ArgumentParser`.

        Attributes:
            parser: set to results of `argparse.ArgumentParser`.

        Side Effects:
            `parser.options.cli` is set `self`.
        """

        kwargs["add_help"] = False  # type: ignore[assignment]
        self.parser = argparse.ArgumentParser(**kwargs)  # type: ignore[arg-type]
        self.parser.set_defaults(cli=self)
        return self.parser

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

    def _parse_args(self) -> argparse.Namespace:
        """Parse command line and return options."""

        options = self.parser.parse_args(self.argv)

        if self._config_error:
            # postponed from init_config
            self.parser.error(str(self._config_error))

        self._update_config_from_options(options)
        return options
