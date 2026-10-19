"""Download TV Maze shows. This is the only module that uses requests."""

import logging

import requests

from tvsummary.errors import DownloadError, ResponseError
from tvsummary.models import Show

logger = logging.getLogger(__name__)


class TvMazeSource:
    """Fetch shows from a TV Maze URL and return Show objects."""

    def __init__(self, url, timeout):
        """Remember where to download from and how long to wait."""
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download the page and return shows plus a malformed-record count.

        Records that are not dictionaries are counted as malformed and are
        not turned into Show objects.
        """
        logger.info("Downloading shows from %s", self.url)
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise DownloadError(f"Could not reach {self.url}.") from exc

        if not isinstance(payload, list):
            raise ResponseError("Expected a JSON list of show records.")

        logger.debug("Received %s records", len(payload))
        shows = []
        skipped = 0
        for item in payload:
            if not isinstance(item, dict):
                skipped += 1
                logger.warning("Skipped a record because it was not a show object")
                continue
            shows.append(Show(item))
        return shows, skipped
