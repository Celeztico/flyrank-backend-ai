import time
import requests
from pathlib import Path
from scraper.cache import read_cache, write_cache
from scraper.config import CACHE_DIR, REQUEST_DELAY, REQUEST_TIMEOUT, USER_AGENT

class FetchError(Exception):
    """Raised when a page cannot be fetched successfully."""

    def __init__(
            self,
            message: str,
            *,
            url: str,
            retryable: bool = False,
    ):
        super().__init__(message)
        self.url = url
        self.retryable = retryable

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
        self.cache_hits = 0

    def fetch(self, url: str) -> str:
        cached = read_cache(self.cache_dir, url)

        if cached is not None:
            self.cache_hits += 1
            print(f"CACHE HIT {url} ({len(cached)} bytes)")
            return cached

        return self._fetch_with_retry(url)

    def _fetch_with_retry(self, url: str) -> str:
        attempts = 0
        max_attempts = 2

        while attempts < max_attempts:
            attempts+=1

            self._wait_before_request()

            try:
                response = requests.get(
                    url,
                    headers={"User-Agent": self.user_agent},
                    timeout=self.timeout,
                )

                response.raise_for_status()

                content = response.text

                write_cache(
                    self.cache_dir,
                    url,
                    content,
                )

                self._last_request_time = time.monotonic()

                if attempts > 1:
                    print(f"RETRY SUCCESS {url}")

                print(f"FETCH      {url} ({len(content)} bytes)")

                return content

            except requests.Timeout as e:
                if attempts < max_attempts:
                    print(f"RETRY      {url} (timeout)")
                    continue

                raise FetchError(f"Timeout fetching {url}",url=url,retryable=True) from e

            except requests.HTTPError as e:
                status_code = e.response.status_code

                if status_code >= 500 and attempts < max_attempts:
                    print(f"RETRY      {url} (HTTP {status_code})")
                    continue

                print(f"FAILED     {url} (HTTP {status_code})")
                raise FetchError(f"HTTP {status_code} fetching {url}", url=url,retryable=status_code >= 500) from e

            except requests.RequestException as e:
                raise FetchError(f"Failed to fetch {url}: {e}",url=url,retryable=False) from e

    def _wait_before_request(self) -> None:
        if self._last_request_time is None:
            return

        elapsed = time.monotonic() - self._last_request_time
        remaining = self.delay - elapsed

        if remaining > 0:
            time.sleep(remaining)