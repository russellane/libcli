from typing import List, Optional

import pytest

from libcli import BaseCLI


class SimpleCLI(BaseCLI):
    """Simple command line interface."""

    def init_parser(self) -> None:
        self.ArgumentParser(
            prog="simple",
            description=self.dedent(
                """
    This is the `SimpleCLI` program.

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

    def main(self) -> None:
        print("Running", self)


def main(args: Optional[List[str]] = None) -> None:
    """Command line interface entry point (function)."""
    return SimpleCLI(args).main()


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
    assert err.value.code == 2


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


def test_debug():
    with pytest.raises(SystemExit) as err:
        main(["-X"])
    assert err.value.code == 0
