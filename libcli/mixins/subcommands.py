"""Subcommand registration mixin for BaseCLI."""

from __future__ import annotations

import argparse
import importlib
import pkgutil
from typing import Any, Callable

__all__ = ["SubcommandMixin"]


class SubcommandMixin:
    """Handles subcommand registration via classes or module discovery."""

    parser: argparse.ArgumentParser
    add_parser: Callable[[Any], argparse.ArgumentParser] | None

    def add_subcommand_classes(self, subcommand_classes: list[Any]) -> None:
        """Add list of subcommands to this parser."""

        # https://docs.python.org/3/library/argparse.html#sub-commands
        self._init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)
        for subcommand_class in subcommand_classes:
            subcommand_class(self)

        # equiv to module: .commands.help import Command as HelpCommand
        # sub = self.add_subcommand_parser("help", help="same as `--help`")
        # sub.set_defaults(cmd=self.parser.print_help)

    def add_subcommand_modules(
        self,
        modname: str,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        """Add all subcommands in module `modname`.

        e.g., cli.add_subcommand_modules("wumpus.commands")
        or,   cli.add_subcommand_modules("wumpus.cli.commands")
        or wherever your command modules are.

        1. Load each module in containing module `modname`,
        2. Instantiate an instance each module's `Command` class, and
        3. Add the command to this cli.

        If all command classes are not named `Command`, then they must all
        begin and/or end with common tags. Pass `prefix` and/or `suffix` to
        specify, and the longest matching class will be used. Multiple
        command classes could be defined in one module this way.

        e.g.,
            wumpus/commands/move.py
                class WumpusMoveCmd(BaseCmd):
                    ...

            wumpus/commands/shoot.py
                class WumpusCmd(BaseCmd):
                    ...
                class WumpusShootCmd(WumpusCmd)
                    ...

            cli.add_subcommand_modules("wumpus.commands", prefix="Wumpus", suffix="Cmd")
        """

        self._init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)

        commands_module_path = importlib.import_module(modname, __name__).__path__
        base_name = (prefix or "") + (suffix or "")

        for modinfo in pkgutil.iter_modules(commands_module_path):
            module = importlib.import_module(f"{modname}.{modinfo.name}", __name__)

            if not prefix and not suffix and hasattr(module, "Command"):
                module.Command(self)
                continue

            for name in [x for x in dir(module) if x != base_name]:
                if prefix and not name.startswith(prefix):
                    continue
                if suffix and not name.endswith(suffix):
                    continue
                try:
                    cmd_class = getattr(module, name)
                except AttributeError:
                    continue
                cmd_class(self)

    def _init_subcommands(self, **kwargs: Any) -> None:
        """Prepare to add subcommands to main parser."""

        subparsers = self.parser.add_subparsers(**kwargs)
        self.add_parser = subparsers.add_parser
