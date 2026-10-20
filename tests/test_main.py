"""The entry point and settings failures, with no network calls."""

import json

import pytest
import requests

from tvsummary import SettingsError, load_settings
from tvsummary.main import main


def _settings_text(folder: str) -> str:
    return "\n".join(
        [
            'source_url = "https://example.invalid/shows"',
            "timeout = 1",
            f'output_folder = "{folder}"',
            "seed = 5005",
            "sample_size = 2",
            'log_level = "INFO"',
            "",
        ]
    )


def test_missing_settings_file_raises(tmp_path):
    missing = tmp_path / "missing.toml"
    with pytest.raises(SettingsError, match="read"):
        load_settings(missing)


def test_incomplete_settings_file_raises(tmp_path):
    partial = tmp_path / "partial.toml"
    partial.write_text('source_url = "https://example.com"\n', encoding="utf-8")
    with pytest.raises(SettingsError, match="missing"):
        load_settings(partial)


def test_failed_download_returns_1_and_prints_error(tmp_path, monkeypatch, capsys):
    config = tmp_path / "settings.toml"
    config.write_text(_settings_text((tmp_path / "out").as_posix()), encoding="utf-8")

    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr("tvsummary.sources.requests.get", fake_get)
    code = main(["--config", str(config)])
    assert code == 1
    error_lines = [
        line
        for line in capsys.readouterr().err.splitlines()
        if line.startswith("Error:")
    ]
    assert len(error_lines) == 1
    assert "reach" in error_lines[0]


def test_missing_config_option_returns_1(capsys):
    code = main(["--config", "config/does-not-exist.toml"])
    assert code == 1
    error_lines = [
        line
        for line in capsys.readouterr().err.splitlines()
        if line.startswith("Error:")
    ]
    assert len(error_lines) == 1
    assert error_lines[0].startswith("Error:")


def test_successful_run_writes_files_and_returns_0(tmp_path, monkeypatch, show_record):
    records = []
    for index in range(50):
        item = dict(show_record)
        item["name"] = f"Show {index}"
        records.append(item)

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return records

    monkeypatch.setattr(
        "tvsummary.sources.requests.get", lambda *args, **kwargs: FakeResponse()
    )
    folder = tmp_path / "out"
    config = tmp_path / "settings.toml"
    config.write_text(_settings_text(folder.as_posix()), encoding="utf-8")
    code = main(["--config", str(config)])
    assert code == 0
    saved = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    info = json.loads((folder / "run_info.json").read_text(encoding="utf-8"))
    assert saved["records_processed"] == 50
    assert len(saved["featured_shows"]) == 2
    assert info["settings"]["seed"] == 5005
    assert info["tools"]["pytest"]
    assert info["tools"]["mypy"]
    assert info["tools"]["ruff"]
