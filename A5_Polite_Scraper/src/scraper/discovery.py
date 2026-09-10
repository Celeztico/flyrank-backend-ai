from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scraper.fetcher import Fetcher

@dataclass(frozen=True)
class DiscoveredBook:
    product_url: str
    source_page: str


@dataclass
class DiscoveryResult:
    catalogue_pages: int
    discovered_books: list[DiscoveredBook]

    @property
    def unique_books(self) -> list[DiscoveredBook]:
        seen = set()
        unique = []

        for book in self.discovered_books:
            if book.product_url in seen:
                continue

            seen.add(book.product_url)
            unique.append(book)

        return unique


class CatalogueDiscovery:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    def extract_book_urls(self, html: str, page_url: str) -> list[DiscoveredBook]:
        soup = BeautifulSoup(html, "html.parser")

        books = []

        for article in soup.select("article.product_pod"):
            link = article.select_one("h3 a")

            if link is None:
                continue

            href = link.get("href")

            if not href:
                continue

            product_url = urljoin(page_url, href)

            books.append(
                DiscoveredBook(
                    product_url=product_url,
                    source_page=page_url,
                )
            )

        return books

    def find_next_page(self, html: str, page_url: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")

        next_link = soup.select_one("li.next a")

        if next_link is None:
            return None

        href = next_link.get("href")

        if not href:
            return None

        return urljoin(page_url, href)

    def discover(self, start_url: str, max_pages: int = 3) -> DiscoveryResult:
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
            discovered_books=all_book_urls,
        )