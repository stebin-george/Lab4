"""Shared fixtures for tests that never use the network."""

import pytest

from tvsummary import Show


@pytest.fixture
def show_record():
    """Return one hand-made show payload with every field filled in."""
    return {
        "name": "Example",
        "genres": ["Drama"],
        "language": "English",
        "rating": {"average": 8},
        "premiered": "2013-06-24",
        "network": {"name": "CBS"},
        "webChannel": None,
    }


@pytest.fixture
def show(show_record):
    """Return a Show built from the hand-made payload."""
    return Show(show_record)
