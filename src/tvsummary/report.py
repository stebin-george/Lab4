"""Build the summary dictionary and write it to JSON."""

import json
import logging
from pathlib import Path

from tvsummary.aggregations import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    ShowsPremieredPerDecade,
    ShowsWithoutBroadcastNetwork,
)
from tvsummary.config import SOURCE_URL
from tvsummary.models import Show

logger = logging.getLogger(__name__)


def build_summary(shows: list[Show], skipped_malformed: int) -> dict[str, object]:
    """Combine every aggregation into one dict ready to write."""
    aggregations = [
        ShowsPerGenre(),
        AverageRatingByLanguage(),
        ShowsPremieredPerDecade(),
        ShowsWithoutBroadcastNetwork(),
    ]
    summary: dict[str, object] = {
        "source_url": SOURCE_URL,
        "records_processed": len(shows),
        "records_skipped_malformed": skipped_malformed,
    }
    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(shows)
    return summary


def write_summary(summary: dict[str, object], path: str | Path) -> None:
    """Write the summary to a JSON file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    destination.write_text(text, encoding="utf-8")
    logger.info("Wrote summary data to %s", destination)
