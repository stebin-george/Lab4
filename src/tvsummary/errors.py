"""Errors this package raises on purpose."""


class TvSummaryError(Exception):
    """Base class for failures the program knows how to explain."""


class DownloadError(TvSummaryError):
    """The show list could not be downloaded."""


class ResponseError(TvSummaryError):
    """The downloaded payload did not have the expected shape."""


class SettingsError(TvSummaryError):
    """The settings file is missing, unreadable, or incomplete."""


class OutputError(TvSummaryError):
    """The summary or run record could not be written."""
