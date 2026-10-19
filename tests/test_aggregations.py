"""One test for each aggregation, using hand-made shows."""

from tvsummary import (
    AverageRatingByLanguage,
    ShowsPerGenre,
    ShowsPremieredPerDecade,
    ShowsWithoutBroadcastNetwork,
)


def test_shows_per_genre_counts_each_genre_and_skips_blanks(show):
    blank = type(show)(
        {
            "name": "No Genre",
            "genres": [],
            "language": "English",
            "rating": {"average": 7},
            "premiered": "2012-01-01",
            "network": {"name": "HBO"},
            "webChannel": None,
        }
    )
    result = ShowsPerGenre().compute([show, blank])
    assert result["shows_without_genre"] == 1
    assert result["counts"]["Drama"] == 1


def test_average_rating_skips_a_missing_rating(show, show_record):
    show_record["rating"] = {"average": None}
    show_record["name"] = "Unrated"
    result = AverageRatingByLanguage().compute([show, type(show)(show_record)])
    assert result["shows_excluded"] == 1
    assert result["averages"]["English"] == 8.0


def test_premieres_are_grouped_by_decade(show, show_record):
    show_record["premiered"] = "bad"
    show_record["name"] = "Undated"
    result = ShowsPremieredPerDecade().compute([show, type(show)(show_record)])
    assert result["counts"] == {"2010s": 1}
    assert result["shows_excluded"] == 1


def test_web_only_shows_are_not_given_a_network(show, show_record):
    show_record["network"] = None
    show_record["webChannel"] = {"name": "Netflix"}
    show_record["name"] = "Streaming"
    result = ShowsWithoutBroadcastNetwork().compute([show, type(show)(show_record)])
    assert result["web_only_shows"] == 1
    assert result["web_channels"] == ["Netflix"]
    assert result["shows_with_neither"] == 0
