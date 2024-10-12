## libcli

Command line interface framework.

The `libcli` package, built on
[argparse](https://docs.python.org/3/library/argparse.html), provides
functions and features that are common to or desired by many command
line applications:

* Colorized help output, with `prog -h`, or `prog --help`.

* Help output in `Markdown` format, with `prog --md-help`.

* Print all help (top command, and all subcommands), with `prog -H`, or
`prog --long-help`. (For commands with subcommands).

* Configure logging, with `-v`, or `--verbose`
(`"-v"`=INFO, `"-vv"`=DEBUG, `"-vvv"`=TRACE). Integrated
with [loguru](https://github.com/Delgan/loguru) and
[logging](https://docs.python.org/3/library/logging.html).

* Print the current version of the application, with `-V`, or `--version`;
uses value from application's package metadata.

* Load configuration from a file, *before* parsing the command line,
with `--config FILE`.  (Well, it parsed at least that much.. and "-v"
for debugging "--config" itself.)  This allows values from the config
file to be available when building the `argparse.ArgumentParser`, for
setting defaults, or including within help strings of arguments/options.

* Print the active configuration, after loading the config file, with `--print-config`.

* Print the application's URL, with `--print-url`;
uses value from application's package metadata.

* Integrate with [argcomplete](https://github.com/kislyuk/argcomplete),
with `--completion`.

* Automatic inclusion of all common options, above.

* Normalized help text of all command line arguments/options.

    * Force the first letter of all help strings to be upper case.
    * Force all help strings to end with a period.

* Provides a function `add_default_to_help` to consistently include
a default value in an argument/option's help string.

* Supports single command applications, and command/sub-commands applications.


### class BaseCLI

Command line interface base class.

$ cat minimal.py

    from libcli import BaseCLI
    class HelloCLI(BaseCLI):
        def main(self) -> None:
            print("Hello")
    if __name__ == "__main__":
        HelloCLI().main()

$ python minimal.py -h

    Usage: minimal.py [-h] [-v] [-V] [--print-config] [--print-url] [--completion [SHELL]]

    General Options:
      -h, --help            Show this help message and exit.
      -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
      -V, --version         Print version number and exit.
      --print-config        Print effective config and exit.
      --print-url           Print project url and exit.
      --completion [SHELL]  Print completion scripts for `SHELL` and exit (default: `bash`).

$ cat simple.py

    from libcli import BaseCLI

    class HelloCLI(BaseCLI):

        def init_parser(self) -> None:
            self.parser = self.ArgumentParser(
                prog=__package__,
                description="This program says hello.",
            )

        def add_arguments(self) -> None:
            self.parser.add_argument(
                "--spanish",
                action="store_true",
                help="Say hello in Spanish.",
            )
            self.parser.add_argument(
                "name",
                help="The person to say hello to.",
            )

        def main(self) -> None:
            if self.options.spanish:
                print(f"Hola, {self.options.name}!")
            else:
                print(f"Hello, {self.options.name}!")

    if __name__ == "__main__":
        HelloCLI().main()

$ python simply.py -h

    Usage: simple.py [--spanish] [-h] [-v] [-V] [--print-config] [--print-url]
                     [--completion [SHELL]] name

    This program says hello.

    Positional Arguments:
      name                  The person to say hello to.

    Options:
      --spanish             Say hello in Spanish.

    General Options:
      -h, --help            Show this help message and exit.
      -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
      -V, --version         Print version number and exit.
      --print-config        Print effective config and exit.
      --print-url           Print project url and exit.
      --completion [SHELL]  Print completion scripts for `SHELL` and exit (default: `bash`).



### class BaseCmd

Base command class; for commands with subcommands.

$ cat complex.py

    from libcli import BaseCLI, BaseCmd

    class EnglishCmd(BaseCmd):

        def init_command(self) -> None:

            parser = self.add_subcommand_parser(
                "english",
                help="Say hello in English",
                description="The `%(prog)s` command says hello in English.",
            )

            parser.add_argument(
                "name",
                help="The person to say hello to.",
            )

        def run(self) -> None:
            print(f"Hello {self.options.name}!")

    class SpanishCmd(BaseCmd):

        def init_command(self) -> None:

            parser = self.add_subcommand_parser(
                "spanish",
                help="Say hello in Spanish",
                description="The `%(prog)s` command says hello in Spanish.",
            )

            parser.add_argument(
                "name",
                help="The person to say hello to.",
            )

        def run(self) -> None:
            print(f"Hola {self.options.name}!")

    class HelloCLI(BaseCLI):

        def init_parser(self) -> None:
            self.parser = self.ArgumentParser(
                prog=__package__,
                description="This program says hello.",
            )

        def add_arguments(self) -> None:
            self.add_subcommand_classes([EnglishCmd, SpanishCmd])

        def main(self) -> None:
            if not self.options.cmd:
                self.parser.print_help()
                self.parser.exit(2, "error: Missing COMMAND")
            self.options.cmd()

    if __name__ == "__main__":
        HelloCLI().main()

$ python complex.py -H

    ---------------------------------- COMPLEX.PY ----------------------------------

    usage: complex.py [-h] [-H] [-v] [-V] [--print-config] [--print-url]
                      [--completion [SHELL]]
                      COMMAND ...

    This program says hello.

    Specify one of:
      COMMAND
        english             Say hello in English.
        spanish             Say hello in Spanish.

    General options:
      -h, --help            Show this help message and exit.
      -H, --long-help       Show help for all commands and exit.
      -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
      -V, --version         Print version number and exit.
      --print-config        Print effective config and exit.
      --print-url           Print project url and exit.
      --completion [SHELL]  Print completion scripts for `SHELL` and exit
                            (default: `bash`).

    ------------------------------ COMPLEX.PY ENGLISH ------------------------------

    usage: complex.py english [-h] name

    The `complex.py english` command says hello in English.

    positional arguments:
      name        The person to say hello to.

    options:
      -h, --help  Show this help message and exit.

    ------------------------------ COMPLEX.PY SPANISH ------------------------------

    usage: complex.py spanish [-h] name

    The `complex.py spanish` command says hello in Spanish.

    positional arguments:
      name        The person to say hello to.

    options:
      -h, --help  Show this help message and exit.



