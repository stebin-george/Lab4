"""Download failures are tested with a stand-in, not the network."""

import json

import pytest
import requests

from tvsummary import DownloadError, ResponseError, TvMazeSource, write_summary


def test_a_failed_download_raises_download_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr("tvsummary.sources.requests.get", fake_get)
    source = TvMazeSource("https://example.invalid", timeout=1)
    with pytest.raises(DownloadError, match="no network"):
        source.fetch()


def test_a_non_list_response_raises_response_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"not": "a list"}

    monkeypatch.setattr(
        "tvsummary.sources.requests.get", lambda *args, **kwargs: FakeResponse()
    )
    source = TvMazeSource("https://example.invalid", timeout=1)
    with pytest.raises(ResponseError, match="JSON list"):
        source.fetch()


def test_records_that_are_not_objects_are_counted_and_skipped(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return [{"name": "Kept", "genres": [], "language": "English"}, "nope"]

    monkeypatch.setattr(
        "tvsummary.sources.requests.get", lambda *args, **kwargs: FakeResponse()
    )
    shows, skipped = TvMazeSource("https://example.invalid", timeout=1).fetch()
    assert skipped == 1
    assert len(shows) == 1
    assert shows[0].name == "Kept"


def test_write_summary_uses_tmp_path(tmp_path):
    destination = tmp_path / "summary.json"
    write_summary({"records_processed": 2}, destination)
    saved = json.loads(destination.read_text(encoding="utf-8"))
    assert saved["records_processed"] == 2
