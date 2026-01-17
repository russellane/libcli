"""Logging mixin for BaseCLI."""

import contextlib
import logging
import sys

__all__ = ["LoggingMixin"]

with contextlib.suppress(ImportError):
    from loguru import logger  # type: ignore


class LoggingMixin:  # pylint: disable=too-few-public-methods
    """Handles logging setup based on verbosity level."""

    def init_logging(self, verbose: int) -> None:
        """Set logging levels based on `--verbose`."""

        if logging.root.handlers:
            return  # already configured

        # stdlib:
        #    (dflt)           -v            -vv
        _ = [logging.WARNING, logging.INFO, logging.DEBUG]
        logging.basicConfig(level=_[min(verbose, len(_) - 1)])

        if "logger" in globals():
            # loguru:
            #    (dflt)  -v       -vv
            _ = ["INFO", "DEBUG", "TRACE"]
            level = _[min(verbose, len(_) - 1)]
            logger.remove()
            logger.add(sys.stderr, level=level)
