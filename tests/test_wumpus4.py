import pytest

from libcli import BaseCLI


class WumpusCLI(BaseCLI):
    """Wumpus command line interface."""

    def init_parser(self) -> None:
        self.ArgumentParser(
            prog="wumpus",
            description=self.dedent(
                """
    Hunt the Wumpus.

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
        self.add_subcommand_modules("tests.wumpus4", prefix="Wumpus", suffix="Cmd")

    def main(self) -> None:

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        self.options.cmd()


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    WumpusCLI(args).main()


if __name__ == "__main__":
    main()

# -------------------------------------------------------------------------------


def test_version() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--version"])
    assert err.value.code == 0


def test_help() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--help"])
    assert err.value.code == 0


def test_md_help() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--md-help"])
    assert err.value.code == 0


def test_long_help() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--long-help"])
    assert err.value.code == 0


def test_bogus_option() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--bogus-option"])
    assert err.value.code == 2


def test_bogus_argument() -> None:
    with pytest.raises(SystemExit) as err:
        main(["bogus-argument"])
    assert err.value.code == 2


def test_print_config() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--print-config"])
    assert err.value.code == 0


def test_print_url() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--print-url"])
    assert err.value.code == 0


# -------------------------------------------------------------------------------


def test_move_help() -> None:
    with pytest.raises(SystemExit) as err:
        main(["move", "--help"])
    assert err.value.code == 0


def test_move_bogus_option() -> None:
    with pytest.raises(SystemExit) as err:
        main(["move", "--bogus-option"])
    assert err.value.code == 2


def test_move_bogus_argument() -> None:
    with pytest.raises(SystemExit) as err:
        main(["move", "bogus-argument"])
    assert err.value.code == 2


def test_move_argument_missing() -> None:
    with pytest.raises(SystemExit) as err:
        main(["move"])
    assert err.value.code == 2


def test_move_argument_ok() -> None:
    main(["move", "12"])


# -------------------------------------------------------------------------------


def test_shoot_help() -> None:
    with pytest.raises(SystemExit) as err:
        main(["shoot", "--help"])
    assert err.value.code == 0


def test_shoot_bogus_option() -> None:
    with pytest.raises(SystemExit) as err:
        main(["shoot", "--bogus-option"])
    assert err.value.code == 2


def test_shoot_bogus_argument() -> None:
    with pytest.raises(SystemExit) as err:
        main(["shoot", "bogus-argument"])
    assert err.value.code == 2


def test_shoot_argument_missing() -> None:
    with pytest.raises(SystemExit) as err:
        main(["shoot"])
    assert err.value.code == 2


def test_shoot_argument_ok() -> None:
    main(["shoot", "7"])
