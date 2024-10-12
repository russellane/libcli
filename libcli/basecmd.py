"""Base command class."""

import argparse
from typing import Any, Callable

from libcli.basecli import BaseCLI

__all__ = ["BaseCmd"]


class BaseCmd:
    """Base command class; for commands with subcommands.

    $ cat complex.py

        from libcli import BaseCLI, BaseCmd

        class EnglishCmd(BaseCmd):

            def init_command(self) -> None:

                parser = self.add_subcommand_parser(
                    "english",
                    help="Say hello in English",
                    description="The `%(prog)s` command says hello in English.",
                )

                parser.add_argument(
                    "name",
                    help="The person to say hello to.",
                )

            def run(self) -> None:
                print(f"Hello {self.options.name}!")

        class SpanishCmd(BaseCmd):

            def init_command(self) -> None:

                parser = self.add_subcommand_parser(
                    "spanish",
                    help="Say hello in Spanish",
                    description="The `%(prog)s` command says hello in Spanish.",
                )

                parser.add_argument(
                    "name",
                    help="The person to say hello to.",
                )

            def run(self) -> None:
                print(f"Hola {self.options.name}!")

        class HelloCLI(BaseCLI):

            def init_parser(self) -> None:
                self.parser = self.ArgumentParser(
                    prog=__package__,
                    description="This program says hello.",
                )

            def add_arguments(self) -> None:
                self.add_subcommand_classes([EnglishCmd, SpanishCmd])

            def main(self) -> None:
                if not self.options.cmd:
                    self.parser.print_help()
                    self.parser.exit(2, "error: Missing COMMAND")
                self.options.cmd()

        if __name__ == "__main__":
            HelloCLI().main()

    $ python complex.py -H

        ---------------------------------- COMPLEX.PY ----------------------------------

        usage: complex.py [-h] [-H] [-v] [-V] [--print-config] [--print-url]
                          [--completion [SHELL]]
                          COMMAND ...

        This program says hello.

        Specify one of:
          COMMAND
            english             Say hello in English.
            spanish             Say hello in Spanish.

        General options:
          -h, --help            Show this help message and exit.
          -H, --long-help       Show help for all commands and exit.
          -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
          -V, --version         Print version number and exit.
          --print-config        Print effective config and exit.
          --print-url           Print project url and exit.
          --completion [SHELL]  Print completion scripts for `SHELL` and exit
                                (default: `bash`).

        ------------------------------ COMPLEX.PY ENGLISH ------------------------------

        usage: complex.py english [-h] name

        The `complex.py english` command says hello in English.

        positional arguments:
          name        The person to say hello to.

        options:
          -h, --help  Show this help message and exit.

        ------------------------------ COMPLEX.PY SPANISH ------------------------------

        usage: complex.py spanish [-h] name

        The `complex.py spanish` command says hello in Spanish.

        positional arguments:
          name        The person to say hello to.

        options:
          -h, --help  Show this help message and exit.

    """

    def __init__(self, cli: BaseCLI) -> None:
        """Initialize base command instance.

        After setting `self.cli`, the constructor calls these public methods,
        which the subclass MAY implement, in order:

            init_command: should call `self.add_subcommand_parser` and `add_argument`.

        Args:
            cli: the CLI.

        Attributes:
            cli: the CLI.
            options: will contain results of `parse_args` when `run` is called.

        """

        self.cli = cli
        self.options: argparse.Namespace
        self.init_command()

    def init_command(self) -> None:
        """Implement in subclass to call `add_subcommand_parser` and `add_argument`."""
        # raise NotImplementedError

    def add_subcommand_parser(self, name: str, **kwargs: Any) -> argparse.ArgumentParser:
        """Add subcommand to main parser and return subcommand's subparser.

        Wrap `argparse.ArgumentParser.add_subparsers.add_parser`.

        Side Effects:
            `parser.options.cmd` is set to call the subcommand's `run` method.
        """

        assert self.cli.add_parser
        parser = self.cli.add_parser(name, **kwargs)
        parser.set_defaults(cmd=lambda: self._promote_options(self.run), prog=name)
        return parser

    def _promote_options(self, run: Callable[[], None]) -> None:
        self.options = self.cli.options
        run()

    def run(self) -> None:
        """Perform the command."""
        # raise NotImplementedError
