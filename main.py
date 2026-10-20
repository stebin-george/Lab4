"""Wire the package together and print success or a download error."""

import sys
from pathlib import Path

from tvsummary import (
    ResponseError,
    TvMazeSource,
    TvSummaryError,
    build_summary,
    load_settings,
    write_summary,
)
from tvsummary.logging_setup import configure_logging
from tvsummary.report import build_run_info, write_json


def main():
    """Download shows, aggregate them, and write the summary."""
    try:
        settings = load_settings("config/tvsummary.toml")
        configure_logging(settings.log_level)
        shows, skipped = TvMazeSource(settings.source_url, settings.timeout).fetch()
        received = len(shows) + skipped
        if received < 50:
            raise ResponseError(f"Expected at least 50 shows, received {received}.")
        summary = build_summary(shows, skipped, settings)
        folder = Path(settings.output_folder)
        write_summary(summary, folder / "summary.json")
        write_json(build_run_info(settings), folder / "run_info.json")
    except TvSummaryError as exc:
        print(f"Download failed: {exc}")
        sys.exit(1)
    print(f"Wrote {summary['records_processed']} shows to {folder / 'summary.json'}.")


if __name__ == "__main__":
    main()
