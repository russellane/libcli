"""Base class for our `HelpAction`s."""

import argparse

__all__ = ["BaseHelpAction"]


class BaseHelpAction(argparse._HelpAction):
    # pylint: disable=protected-access
    # pylint: disable=too-few-public-methods
    """Base class for our `HelpAction`s."""
