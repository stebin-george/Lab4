"""Summarize one page of TV Maze shows."""

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    ShowsPerGenre,
    ShowsPremieredPerDecade,
    ShowsWithoutBroadcastNetwork,
)
from tvsummary.errors import (
    DownloadError,
    OutputError,
    ResponseError,
    SettingsError,
    TvSummaryError,
)
from tvsummary.models import Show
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TvMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "DownloadError",
    "OutputError",
    "ResponseError",
    "SettingsError",
    "Show",
    "TvSummaryError",
    "ShowsPerGenre",
    "ShowsPremieredPerDecade",
    "ShowsWithoutBroadcastNetwork",
    "TvMazeSource",
    "build_summary",
    "write_summary",
]
