"""Command line interface framework.

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
"""

from libcli.basecli import BaseCLI  # noqa
from libcli.basecmd import BaseCmd  # noqa

__all__ = ["BaseCLI", "BaseCmd"]
