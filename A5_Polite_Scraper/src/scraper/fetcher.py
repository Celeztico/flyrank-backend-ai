import time
import requests
from pathlib import Path
from scraper.cache import read_cache, write_cache
from scraper.config import CACHE_DIR, REQUEST_DELAY, REQUEST_TIMEOUT, USER_AGENT

class FetchError(Exception):
    """Raised when a page cannot be fetched successfully."""

class Fetcher:
    def __init__(
            self,
            cache_dir: Path = CACHE_DIR,
            timeout: float = REQUEST_TIMEOUT,
            delay: float = REQUEST_DELAY,
            user_agent: str = USER_AGENT,
    ):
        self.cache_dir = cache_dir
        self.timeout = timeout
        self.delay = delay
        self.user_agent = user_agent
        self._last_request_time: float | None = None

    def fetch(self, url: str) -> str:
        cached = read_cache(self.cache_dir, url)

        if cached is not None:
            print(f"CACHE HIT {url} ({len(cached)} bytes)")
            return cached

        self._wait_before_request()

        try:
            response = requests.get(
                url,
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise FetchError(f"Failed to fetch {url}: {e}") from e

        content = response.text

        write_cache(self.cache_dir, url, content)

        self._last_request_time = time.monotonic()

        print(f"FETCH   {url} ({len(content)} bytes)")

        return content

    def _wait_before_request(self) -> None:
        if self._last_request_time is None:
            return

        elapsed = time.monotonic() - self._last_request_time
        remaining = self.delay - elapsed

        if remaining > 0:
            time.sleep(remaining)