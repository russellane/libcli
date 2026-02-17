"""Tests for nested subcommands."""

import pytest

from libcli import BaseCLI, BaseCmd


# Nested commands: myapp remote add / myapp remote remove
class RemoteAddCmd(BaseCmd):
    """Add a remote."""

    def init_command(self) -> None:
        parser = self.add_subcommand_parser("add", help="Add a remote")
        parser.add_argument("name", help="Remote name")
        parser.add_argument("url", help="Remote URL")

    def run(self) -> None:
        pass


class RemoteRemoveCmd(BaseCmd):
    """Remove a remote."""

    def init_command(self) -> None:
        parser = self.add_subcommand_parser(
            "remove",
            aliases=["rm"],
            help="Remove a remote",
        )
        parser.add_argument("name", help="Remote name")

    def run(self) -> None:
        pass


class RemoteCmd(BaseCmd):
    """Remote command group."""

    def init_command(self) -> None:
        self.add_subcommand_parser("remote", help="Manage remotes")
        self.add_subcommand_classes([RemoteAddCmd, RemoteRemoveCmd])

    def run(self) -> None:
        # Called if no subcommand given
        self.parser.print_help()


class StatusCmd(BaseCmd):
    """Simple status command (not nested)."""

    def init_command(self) -> None:
        self.add_subcommand_parser("status", help="Show status")

    def run(self) -> None:
        pass


class NestedCLI(BaseCLI):
    """CLI with nested commands."""

    def add_arguments(self) -> None:
        self.add_subcommand_classes([RemoteCmd, StatusCmd])

    def main(self) -> None:
        if self.options.cmd:
            self.options.cmd()


def test_nested_remote_add() -> None:
    """Test nested command: remote add."""
    cli = NestedCLI(["remote", "add", "origin", "https://github.com/foo/bar"])
    assert cli.options.name == "origin"
    assert cli.options.url == "https://github.com/foo/bar"


def test_nested_remote_remove() -> None:
    """Test nested command: remote remove."""
    cli = NestedCLI(["remote", "remove", "origin"])
    assert cli.options.name == "origin"


def test_nested_remote_remove_alias() -> None:
    """Test nested command with alias: remote rm."""
    cli = NestedCLI(["remote", "rm", "origin"])
    assert cli.options.name == "origin"


def test_simple_command() -> None:
    """Test non-nested command still works."""
    cli = NestedCLI(["status"])
    assert cli.options.cmd is not None


def test_nested_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test help shows nested structure."""
    with pytest.raises(SystemExit):
        NestedCLI(["--help"])

    captured = capsys.readouterr()
    print(captured.out)
    assert "remote" in captured.out
    assert "status" in captured.out


def test_nested_subcommand_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test help for nested command shows its subcommands."""
    with pytest.raises(SystemExit):
        NestedCLI(["remote", "--help"])

    captured = capsys.readouterr()
    print(captured.out)
    assert "add" in captured.out
    assert "remove" in captured.out


def test_nested_subcommand_sub_help() -> None:
    """Test help for nested command shows its subcommands."""
    with pytest.raises(SystemExit):
        NestedCLI(["remote", "add", "--help"])
