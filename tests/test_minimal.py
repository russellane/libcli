import sys

import pytest

from libcli import BaseCLI


class MinimalCLI(BaseCLI):
    """Minimal command line interface."""

    def main(self) -> None:
        print("Running", self)


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    sys.argv = ["minimal"]
    MinimalCLI(args).main()


def test_no_args() -> None:
    main()


def _test_none_args() -> None:
    main(None)


def _test_empty_args() -> None:
    main([])


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
    assert err.value.code == 2


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


def test_debug() -> None:
    with pytest.raises(SystemExit) as err:
        main(["-X"])
    assert err.value.code == 0


def test_completion() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--completion"])
    assert err.value.code == 0


def test_completion_bogus() -> None:
    with pytest.raises(SystemExit) as err:
        main(["--completion", "bogus"])
    assert err.value.code == 2


@pytest.mark.parametrize("shell", ["bash", "fish", "tcsh"])
def test_completion_shell(shell: str) -> None:
    with pytest.raises(SystemExit) as err:
        main(["--completion", shell])
    assert err.value.code == 0
