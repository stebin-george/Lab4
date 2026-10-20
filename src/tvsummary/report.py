"""Build the summary dictionary and write it to JSON."""

import importlib.metadata
import json
import logging
import platform
import random
from pathlib import Path

from tvsummary.aggregations import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    ShowsPremieredPerDecade,
    ShowsWithoutBroadcastNetwork,
)
from tvsummary.config import Settings
from tvsummary.errors import OutputError, SettingsError
from tvsummary.models import Show

logger = logging.getLogger(__name__)


def featured_show_names(shows: list[Show], seed: int, sample_size: int) -> list[str]:
    """Choose show names with random.Random so the same seed repeats."""
    names = [
        show.name.strip()
        for show in shows
        if isinstance(show.name, str) and show.name.strip()
    ]
    if sample_size > len(names):
        raise SettingsError(
            f"sample_size {sample_size} is larger than the {len(names)} named shows."
        )
    return random.Random(seed).sample(names, sample_size)


def build_summary(
    shows: list[Show], skipped_malformed: int, settings: Settings
) -> dict[str, object]:
    """Combine every aggregation into one dict ready to write."""
    aggregations = [
        ShowsPerGenre(),
        AverageRatingByLanguage(),
        ShowsPremieredPerDecade(),
        ShowsWithoutBroadcastNetwork(),
    ]
    summary: dict[str, object] = {
        "source_url": settings.source_url,
        "records_processed": len(shows),
        "records_skipped_malformed": skipped_malformed,
    }
    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(shows)
    summary["featured_shows"] = featured_show_names(
        shows, settings.seed, settings.sample_size
    )
    return summary


def build_run_info(settings: Settings) -> dict[str, object]:
    """Record the settings and tool versions used for one run."""
    return {
        "settings": {
            "source_url": settings.source_url,
            "timeout": settings.timeout,
            "output_folder": settings.output_folder,
            "seed": settings.seed,
            "sample_size": settings.sample_size,
            "log_level": settings.log_level,
        },
        "python_version": platform.python_version(),
        "tools": {
            "pytest": _tool_version("pytest"),
            "mypy": _tool_version("mypy"),
            "ruff": _tool_version("ruff"),
        },
    }


def write_summary(summary: dict[str, object], path: str | Path) -> None:
    """Write the summary to a JSON file."""
    write_json(summary, path)


def write_json(payload: dict[str, object], path: str | Path) -> None:
    """Write one JSON object, creating parent folders if needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    try:
        destination.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise OutputError(f"Could not write {destination}.") from exc
    logger.info("Wrote %s", destination)


def _tool_version(name: str) -> str:
    """Return an installed tool's version."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError as exc:
        raise SettingsError(f"Required tool {name} is not installed.") from exc
