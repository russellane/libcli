import os
from tempfile import mkstemp
from typing import Iterator

import pytest

from libcli import BaseCLI


@pytest.fixture(name="config_file")
def config_file_() -> Iterator[str]:
    fd, name = mkstemp()
    with os.fdopen(fd, mode="w", encoding="utf-8") as fp:
        fp.write(
            BaseCLI.dedent(
                """
                [myapp]
                name = "Rumpelstiltskin"
                value = 42
                """
            )
        )
        fp.close()
        yield name
    #
    os.unlink(name)


def test_print_config_enoent() -> None:

    class CLI(BaseCLI):
        pass

    with pytest.raises(SystemExit) as err:
        CLI(["--config", "./cant/find/me"])
    assert err.value.code == 2


def test_print_config(config_file: str) -> None:

    class CLI(BaseCLI):
        config = {
            "config-name": "myapp",
        }

        def add_arguments(self) -> None:
            # This is the final public hook before `parse_args` is called.
            import pprint

            pprint.pprint(self.config)
            assert self.config["name"] == "Rumpelstiltskin"
            assert self.config["value"] == 42

    with pytest.raises(SystemExit) as err:
        CLI(["--config", config_file, "--print-config"])
    assert err.value.code == 0
