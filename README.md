# TV Maze Show Summary

This package downloads one page of TV shows and summarizes them by genre, language, premiere decade, and broadcast network. A seeded random sample adds a short list of featured shows, so the same settings produce the same list.

## Setup

```bash
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python -m tvsummary.main
python -m tvsummary.main --config config/tvsummary.toml
```

## Check it

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

## Settings

- `source_url` is the TV Maze page that is downloaded.
- `timeout` is how many seconds to wait for that download.
- `output_folder` is where `summary.json` and `run_info.json` are written.
- `seed` is the random seed used to choose featured shows.
- `sample_size` is how many featured shows are chosen.
- `log_level` is how much detail is written to the log.

## Errors and exit codes

| Error | When it is raised | What the user sees |
| --- | --- | --- |
| `DownloadError` | The download fails, times out, or the server returns an HTTP error | `Error: Could not reach ...` |
| `ResponseError` | The payload is not a list of shows, or fewer than 50 records arrive | `Error: Expected a JSON list of show records.` or `Error: Expected at least 50 shows, received ...` |
| `SettingsError` | The settings file is missing, unreadable, invalid, or incomplete, the sample is larger than the named shows, or pytest, mypy, or ruff is not installed | `Error: Could not read settings file ...` or `Error: Settings file ... is missing ...` |
| `OutputError` | The summary or run record cannot be written | `Error: Could not write ...` |

Exit code 0 means the summary and run record were written. Exit code 1 means one of those errors stopped the run. The program logs the error and prints one line beginning with `Error:` to standard error. It does not print a traceback.

## Reproducing a run

The seed is `seed` in `config/tvsummary.toml`. `run_info.json`, written next to `summary.json`, records the settings used for that run, the Python version, and the installed versions of pytest, mypy, and ruff. Featured shows are chosen with `random.Random(seed)` from the show names in download order. A classmate gets the same `featured_shows` list with the same settings file and the same page of TV Maze records. The random sample uses the Python standard library, so no extra package is required for that step. If TV Maze changes page 0, the list can change even when the seed stays the same.

## What the tests cover

The tests check that a show with no genre list or no rating is cleaned rather than counted as a real value, that each aggregation handles hand-made records, that a failed download and a bad payload raise package errors, that a skipped record is logged, that a missing or incomplete settings file raises `SettingsError`, that `main` returns 1 and prints one `Error:` line when the run cannot finish, that the summary can be written to a temporary folder, and that the same seed produces the same featured shows. They do not call the live TV Maze API. A test that needs wifi fails for the wrong reason, so the live download is checked by running the program instead.

## Known limitations

The package reads only page 0, so the averages describe that page and not every show on TV Maze. Ratings are TV Maze user scores. The featured list follows the order of that page, which TV Maze can change. The Japanese average is based on only a few shows.
