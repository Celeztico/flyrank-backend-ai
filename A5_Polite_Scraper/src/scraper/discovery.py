from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scraper.fetcher import Fetcher

@dataclass
class DiscoveryResult:
    catalogue_pages: int
    discovered_urls: list[str]

    @property
    def unique_urls(self) -> list[str]:
        return list(dict.fromkeys(self.discovered_urls))


class CatalogueDiscovery:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    def extract_book_urls(self, html: str, page_url: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")

        book_urls = []

        for article in soup.select("article.product_pod"):
            link = article.select_one("h3 a")

            if link is None:
                continue

            href = link.get("href")

            if not href:
                continue

            book_urls.append(urljoin(page_url, href))

        return book_urls

    def find_next_page(self, html: str, page_url: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")

        next_link = soup.select_one("li.next a")

        if next_link is None:
            return None

        href = next_link.get("href")

        if not href:
            return None

        return urljoin(page_url, href)

    def discover(self, start_url: str, max_pages: int = 3) -> list[str]:
        current_url = start_url
        all_book_urls = []
        catalogue_pages = 0

        for _ in range(max_pages):
            html = self.fetcher.fetch(current_url)

            catalogue_pages += 1

            book_urls = self.extract_book_urls(html, current_url)
            all_book_urls.extend(book_urls)

            next_url = self.find_next_page(html, current_url)

            if next_url is None:
                break

            current_url = next_url

        return DiscoveryResult(
            catalogue_pages=catalogue_pages,
            discovered_urls=all_book_urls,
        )