"""Tests for the Show record class."""

import pytest

from tvsummary import Show


def test_missing_genre_list_becomes_an_empty_set(show_record):
    show_record["genres"] = None
    assert Show(show_record).genres == frozenset()


def test_missing_rating_is_not_stored_as_zero(show_record):
    show_record["rating"] = {"average": None}
    assert Show(show_record).rating is None


def test_repeated_genres_are_stored_once(show_record):
    show_record["genres"] = ["Drama", " Drama ", "Drama", ""]
    assert Show(show_record).genres == frozenset({"Drama"})


def test_blank_name_reads_as_untitled(show_record):
    show_record["name"] = "   "
    show_record["premiered"] = "not-a-date"
    assert str(Show(show_record)) == "Untitled show"


@pytest.mark.parametrize(
    ("premiered", "expected"),
    [
        ("2013-06-24", 2013),
        ("not-a-date", None),
        ("1899-01-01", None),
        (None, None),
    ],
)
def test_premiere_year_keeps_only_a_usable_year(show_record, premiered, expected):
    show_record["premiered"] = premiered
    assert Show(show_record).premiere_year == expected
