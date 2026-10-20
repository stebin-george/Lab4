"""Summarize one page of TV Maze shows."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerGenre,
    ShowsPremieredPerDecade,
    ShowsWithoutBroadcastNetwork,
)
from tvsummary.config import Settings, load_settings
from tvsummary.errors import (
    DownloadError,
    OutputError,
    ResponseError,
    SettingsError,
    TvSummaryError,
)
from tvsummary.models import Show
from tvsummary.report import build_summary, featured_show_names, write_summary
from tvsummary.sources import TvMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "DownloadError",
    "OutputError",
    "ResponseError",
    "SettingsError",
    "Settings",
    "Show",
    "TvSummaryError",
    "ShowsPerGenre",
    "ShowsPremieredPerDecade",
    "ShowsWithoutBroadcastNetwork",
    "TvMazeSource",
    "build_summary",
    "featured_show_names",
    "load_settings",
    "write_summary",
]
