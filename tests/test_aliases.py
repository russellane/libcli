"""Tests for command aliases."""

import pytest

from libcli import BaseCLI, BaseCmd


class MoveCmd(BaseCmd):
    """Move command with alias."""

    def init_command(self) -> None:
        parser = self.add_subcommand_parser(
            "move",
            aliases=["mv"],
            help="Move a file",
        )
        parser.add_argument("src")
        parser.add_argument("dst")

    def run(self) -> None:
        pass


class RemoveCmd(BaseCmd):
    """Remove command with multiple aliases."""

    def init_command(self) -> None:
        parser = self.add_subcommand_parser(
            "remove",
            aliases=["rm", "delete", "del"],
            help="Remove a file",
        )
        parser.add_argument("path")

    def run(self) -> None:
        pass


class AliasCLI(BaseCLI):
    """CLI with aliased commands."""

    def add_arguments(self) -> None:
        self.add_subcommand_classes([MoveCmd, RemoveCmd])

    def main(self) -> None:
        if self.options.cmd:
            self.options.cmd()


def test_alias_primary_name() -> None:
    """Test command works with primary name."""
    cli = AliasCLI(["move", "a.txt", "b.txt"])
    assert cli.options.src == "a.txt"
    assert cli.options.dst == "b.txt"


def test_alias_short_name() -> None:
    """Test command works with alias."""
    cli = AliasCLI(["mv", "a.txt", "b.txt"])
    assert cli.options.src == "a.txt"
    assert cli.options.dst == "b.txt"


def test_alias_multiple() -> None:
    """Test command with multiple aliases."""
    # All these should work
    for cmd in ["remove", "rm", "delete", "del"]:
        cli = AliasCLI([cmd, "/tmp/foo"])
        assert cli.options.path == "/tmp/foo"


def test_alias_in_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that aliases appear in help output."""
    with pytest.raises(SystemExit):
        AliasCLI(["--help"])

    captured = capsys.readouterr()
    # Aliases should be shown in help
    assert "move" in captured.out
    assert "remove" in captured.out
