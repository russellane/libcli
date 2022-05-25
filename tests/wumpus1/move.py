from libcli import BaseCmd


class Command(BaseCmd):
    """Move subcommand of Wumpus."""

    def init_command(self) -> None:

        parser = self.add_subcommand_parser(
            "move",
            help="help for the `move` command",
            description="Description of the `%(prog)s` command.",
        )

        parser.add_argument("room", type=int, help="help for `ROOM`")

    def run(self) -> None:
        print(f"Move to room {self.options.room}")
