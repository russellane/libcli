"""Tests for environment variable support."""

import pytest

from libcli import BaseCLI


def test_env_verbose(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that MYAPP_VERBOSE env var sets verbosity."""

    class CLI(BaseCLI):
        config = {"config-name": "myapp"}

        def main(self) -> None:
            pass

    # Without env var, verbose defaults to 0
    cli = CLI([])
    assert cli.options.verbose == 0

    # With env var set, verbose uses env value
    monkeypatch.setenv("MYAPP_VERBOSE", "2")
    cli = CLI([])
    assert cli.options.verbose == 2

    # CLI arg overrides env var
    cli = CLI(["-v"])
    assert cli.options.verbose == 3  # 2 from env + 1 from -v


def test_env_default_types() -> None:
    """Test env_default with different types."""

    class CLI(BaseCLI):
        config = {"config-name": "testapp"}

        def main(self) -> None:
            pass

    cli = CLI([])

    # Test with no env var set
    assert cli.env_default("missing", 42, int) == 42
    assert cli.env_default("missing", "default") == "default"
    assert cli.env_default("missing", False, bool) is False


def test_env_default_bool(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test env_default bool parsing."""

    class CLI(BaseCLI):
        config = {"config-name": "testapp"}

        def main(self) -> None:
            pass

    cli = CLI([])

    # Test various truthy values
    for val in ("1", "true", "True", "TRUE", "yes", "YES", "on", "ON"):
        monkeypatch.setenv("TESTAPP_DEBUG", val)
        assert cli.env_default("debug", False, bool) is True

    # Test falsy values
    for val in ("0", "false", "no", "off", ""):
        monkeypatch.setenv("TESTAPP_DEBUG", val)
        assert cli.env_default("debug", True, bool) is False


def test_env_prefix_custom() -> None:
    """Test custom env-prefix."""

    class CLI(BaseCLI):
        config = {"env-prefix": "MYCLI"}

        def main(self) -> None:
            pass

    cli = CLI([])
    assert cli.env_prefix == "MYCLI"


def test_env_prefix_from_config_name() -> None:
    """Test env_prefix derived from config-name."""

    class CLI(BaseCLI):
        config = {"config-name": "my-app"}

        def main(self) -> None:
            pass

    cli = CLI([])
    assert cli.env_prefix == "MY_APP"


def test_env_auto_custom_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test automatic env var binding for custom arguments."""

    class CLI(BaseCLI):
        config = {"config-name": "myapp"}

        def add_arguments(self) -> None:
            self.parser.add_argument("--retries", type=int, default=3)
            self.parser.add_argument("--debug", action="store_true")
            self.parser.add_argument("--name", default="world")

        def main(self) -> None:
            pass

    # Without env vars, use defaults
    cli = CLI([])
    assert cli.options.retries == 3
    assert cli.options.debug is False
    assert cli.options.name == "world"

    # With env vars, use env values automatically
    monkeypatch.setenv("MYAPP_RETRIES", "10")
    monkeypatch.setenv("MYAPP_DEBUG", "true")
    monkeypatch.setenv("MYAPP_NAME", "claude")
    cli = CLI([])
    assert cli.options.retries == 10
    assert cli.options.debug is True
    assert cli.options.name == "claude"

    # CLI args override env vars
    cli = CLI(["--retries", "5", "--name", "user"])
    assert cli.options.retries == 5
    assert cli.options.debug is True  # still from env
    assert cli.options.name == "user"
