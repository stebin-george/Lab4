"""Load run settings from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from tvsummary.errors import SettingsError

_REQUIRED = (
    "source_url",
    "timeout",
    "output_folder",
    "seed",
    "sample_size",
    "log_level",
)
_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True)
class Settings:
    """The values a run reads from its TOML file."""

    source_url: str
    timeout: float
    output_folder: str
    seed: int
    sample_size: int
    log_level: str


def load_settings(path: str | Path) -> Settings:
    """Read a TOML file into a frozen Settings object."""
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise SettingsError(f"Could not read settings file {source}.") from exc
    try:
        loaded = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise SettingsError(f"Settings file {source} is not valid TOML.") from exc

    data = _as_table(loaded, source)
    missing = [key for key in _REQUIRED if key not in data]
    if missing:
        joined = ", ".join(missing)
        raise SettingsError(f"Settings file {source} is missing {joined}.")
    return Settings(
        source_url=_text(data, "source_url"),
        timeout=_timeout(data),
        output_folder=_text(data, "output_folder"),
        seed=_whole_number(data, "seed"),
        sample_size=_sample_size(data),
        log_level=_log_level(data),
    )


def _as_table(loaded: object, source: Path) -> dict[str, object]:
    """Return the TOML document as a string-keyed table."""
    if not isinstance(loaded, dict):
        raise SettingsError(f"Settings file {source} must be a table.")
    table: dict[str, object] = {}
    for key, value in loaded.items():
        if not isinstance(key, str):
            raise SettingsError(f"Settings file {source} has a non-string key.")
        table[key] = value
    return table


def _text(data: dict[str, object], key: str) -> str:
    """Return one non-empty string setting."""
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        raise SettingsError(f"Setting {key} must be a non-empty string.")
    return value


def _timeout(data: dict[str, object]) -> float:
    """Return the timeout as a positive number of seconds."""
    value = data["timeout"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SettingsError("Setting timeout must be a number.")
    if value <= 0:
        raise SettingsError("Setting timeout must be greater than zero.")
    return float(value)


def _whole_number(data: dict[str, object], key: str) -> int:
    """Return one integer setting."""
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise SettingsError(f"Setting {key} must be a whole number.")
    return value


def _sample_size(data: dict[str, object]) -> int:
    """Return how many featured shows to choose."""
    value = _whole_number(data, "sample_size")
    if value < 1:
        raise SettingsError("Setting sample_size must be at least 1.")
    return value


def _log_level(data: dict[str, object]) -> str:
    """Return a logging level name."""
    value = _text(data, "log_level").upper()
    if value not in _LOG_LEVELS:
        allowed = ", ".join(sorted(_LOG_LEVELS))
        raise SettingsError(f"Setting log_level must be one of {allowed}.")
    return value
