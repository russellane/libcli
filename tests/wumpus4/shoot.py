from libcli import BaseCmd


class WumpusShootCmd(BaseCmd):
    """Shoot subcommand of Wumpus."""

    def init_command(self) -> None:

        parser = self.add_subcommand_parser(
            "shoot",
            help="help for the `shoot` command",
            description="Description of the `%(prog)s` command.",
        )

        parser.add_argument("room", type=int, help="help for `ROOM`")

    def run(self) -> None:
        print(f"Shoot to room {self.options.room}")
