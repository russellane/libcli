from pathlib import Path
from typing import List, Optional

import pytest

from libcli import BaseCLI, BaseCmd


class ComplexCLI(BaseCLI):
    """Complex command line interface."""

    def init_parser(self) -> None:
        self.ArgumentParser(
            prog="complex",
            description=self.dedent(
                """
    This is the `ComplexCLI` program.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut `labore et dolore` magna aliqua. Ut enim ad minim
    veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
    velit `esse cillum dolore eu` fugiat nulla pariatur. Excepteur sint
    occaecat cupidatat non proident, sunt in culpa qui officia deserunt
    mollit anim id est laborum.
                """
            ),
        )

    def add_arguments(self) -> None:
        self.add_subcommand_classes([FirstCmd, SecondCmd])

    def main(self) -> None:

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        self.options.cmd()


def main(args: Optional[List[str]] = None) -> None:
    """Command line interface entry point (function)."""
    return ComplexCLI(args).main()


class FirstCmd(BaseCmd):
    """First subcommand of ComplexCLI."""

    def init_command(self) -> None:

        parser = self.add_subcommand_parser(
            "first",
            help="help for the `first` command",
            description="Description of the `%(prog)s` command.",
        )

        parser.add_argument("--first-opt", help="help for `--first-opt`")

    def run(self) -> None:
        print("Running", self)


class SecondCmd(BaseCmd):
    """Second subcommand of ComplexCLI."""

    def init_command(self) -> None:

        parser = self.add_subcommand_parser(
            "second",
            help="help for the `second` command",
            description="Description of the `%(prog)s` command.",
        )

        parser.add_argument("--second-opt", help="help for `--second-opt`")

        arg = parser.add_argument(
            "--path-opt",
            default=Path.home() / "username" / "should" / "be" / "masked",
            help="help for `--path-opt`.",  # note trailing period
        )
        self.cli.add_default_to_help(arg, parser)

        arg = parser.add_argument(
            "--bool-opt",
            action="store_true",
            default=True,
            help="help for `--bool-opt`",  # note no trailing period
        )
        self.cli.add_default_to_help(arg, parser)

    def run(self) -> None:
        print("Running", self)


# -------------------------------------------------------------------------------


def test_version():
    with pytest.raises(SystemExit) as err:
        main(["--version"])
    assert err.value.code == 0


def test_help():
    with pytest.raises(SystemExit) as err:
        main(["--help"])
    assert err.value.code == 0


def test_md_help():
    with pytest.raises(SystemExit) as err:
        main(["--md-help"])
    assert err.value.code == 0


def test_long_help():
    with pytest.raises(SystemExit) as err:
        main(["--long-help"])
    assert err.value.code == 0


def test_bogus_option():
    with pytest.raises(SystemExit) as err:
        main(["--bogus-option"])
    assert err.value.code == 2


def test_bogus_argument():
    with pytest.raises(SystemExit) as err:
        main(["bogus-argument"])
    assert err.value.code == 2


def test_print_config():
    with pytest.raises(SystemExit) as err:
        main(["--print-config"])
    assert err.value.code == 0


def test_print_url():
    with pytest.raises(SystemExit) as err:
        main(["--print-url"])
    assert err.value.code == 0


# -------------------------------------------------------------------------------


def test_first_help():
    with pytest.raises(SystemExit) as err:
        main(["first", "--help"])
    assert err.value.code == 0


def test_first_bogus_option():
    with pytest.raises(SystemExit) as err:
        main(["first", "--bogus-option"])
    assert err.value.code == 2


def test_first_bogus_argument():
    with pytest.raises(SystemExit) as err:
        main(["first", "bogus-argument"])
    assert err.value.code == 2


def test_first():
    main(["first"])


def test_first_option_missing():
    with pytest.raises(SystemExit) as err:
        main(["first", "--first-opt"])
    assert err.value.code == 2


def test_first_option_ok():
    main(["first", "--first-opt", "hello"])


# -------------------------------------------------------------------------------


def test_second_help():
    with pytest.raises(SystemExit) as err:
        main(["second", "--help"])
    assert err.value.code == 0


def test_second_bogus_option():
    with pytest.raises(SystemExit) as err:
        main(["second", "--bogus-option"])
    assert err.value.code == 2


def test_second_bogus_argument():
    with pytest.raises(SystemExit) as err:
        main(["second", "bogus-argument"])
    assert err.value.code == 2


def test_second():
    main(["second"])


def test_second_option_missing():
    with pytest.raises(SystemExit) as err:
        main(["second", "--second-opt"])
    assert err.value.code == 2


def test_second_option_ok():
    main(["second", "--second-opt", "hello"])
