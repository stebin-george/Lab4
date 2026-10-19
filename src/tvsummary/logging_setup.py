"""Configure logging once for a run."""

import logging


def configure_logging(level):
    """Send log records to the console at the given level."""
    numeric = getattr(logging, str(level).upper(), None)
    if not isinstance(numeric, int):
        numeric = logging.INFO
    logging.basicConfig(level=numeric, format="%(levelname)s %(name)s: %(message)s")
