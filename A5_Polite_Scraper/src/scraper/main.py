from scraper.fetcher import Fetcher
from scraper.discovery import CatalogueDiscovery
from scraper.extractor import BookExtractor
from scraper.config import BASE_URL
from datetime import datetime, timezone

def main():
    fetcher = Fetcher()
    discovery = CatalogueDiscovery(fetcher)
    extractor = BookExtractor()

    result = discovery.discover(BASE_URL, max_pages=3)

    records = []

    for book in result.unique_books:
        detail_html = fetcher.fetch(book.product_url)

        fetched_at = datetime.now(timezone.utc).isoformat()

        record = extractor.extract(
            html=detail_html,
            product_url=book.product_url,
            source_page=book.source_page,
            fetched_at=fetched_at,
        )

        records.append(record)

    print(f"detail_pages={len(records)}")

    if records:
        print(records[0])

    

if __name__ == "__main__":
    main()