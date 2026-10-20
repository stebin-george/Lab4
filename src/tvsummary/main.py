"""Entry point for python -m tvsummary.main."""

import argparse
import logging
import sys
from pathlib import Path

from tvsummary.config import load_settings
from tvsummary.errors import ResponseError, TvSummaryError
from tvsummary.logging_setup import configure_logging
from tvsummary.report import build_run_info, build_summary, write_json, write_summary
from tvsummary.sources import TvMazeSource

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Download shows, write the summary, and return an exit code."""
    parser = argparse.ArgumentParser(description="Summarize TV Maze shows.")
    parser.add_argument(
        "--config",
        default="config/tvsummary.toml",
        help="Path to the TOML settings file.",
    )
    args = parser.parse_args(argv)
    try:
        settings = load_settings(args.config)
    except TvSummaryError as exc:
        configure_logging("ERROR")
        return _report_failure(exc)
    configure_logging(settings.log_level)
    try:
        logger.info("Starting a run with seed %s", settings.seed)
        shows, skipped = TvMazeSource(settings.source_url, settings.timeout).fetch()
        received = len(shows) + skipped
        if received < 50:
            raise ResponseError(f"Expected at least 50 shows, received {received}.")
        summary = build_summary(shows, skipped, settings)
        folder = Path(settings.output_folder)
        summary_path = folder / "summary.json"
        write_summary(summary, summary_path)
        write_json(build_run_info(settings), folder / "run_info.json")
    except TvSummaryError as exc:
        return _report_failure(exc)
    print(f"Wrote {summary['records_processed']} shows to {summary_path}.")
    return 0


def _report_failure(exc: TvSummaryError) -> int:
    """Log one expected failure and print the line the user should read."""
    logger.error("%s", exc)
    print(f"Error: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
