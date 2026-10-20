"""Settings failures do not need a network connection."""

import pytest

from tvsummary import SettingsError, load_settings


def test_missing_settings_file_raises(tmp_path):
    missing = tmp_path / "missing.toml"
    with pytest.raises(SettingsError, match="read"):
        load_settings(missing)


def test_incomplete_settings_file_raises(tmp_path):
    partial = tmp_path / "partial.toml"
    partial.write_text('source_url = "https://example.com"\n', encoding="utf-8")
    with pytest.raises(SettingsError, match="missing"):
        load_settings(partial)
