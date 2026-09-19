from scraper.fetcher import Fetcher
from scraper.discovery import CatalogueDiscovery
from scraper.extractor import BookExtractor
from scraper.normalizer import normalize_record
from scraper.schemas import BookRecord
from scraper.storage import write_json
from scraper.config import BASE_URL, OUTPUT_DIR
from datetime import datetime, timezone
from pydantic import ValidationError

def main():
    fetcher = Fetcher()
    discovery = CatalogueDiscovery(fetcher)
    extractor = BookExtractor()

    result = discovery.discover(BASE_URL, max_pages=3)
    unique_books = result.unique_books

    valid_records = []
    errors = []

    for book in unique_books:
        try:
            detail_html = fetcher.fetch(book.product_url)
            fetched_at = datetime.now(timezone.utc).isoformat()

            raw_record = extractor.extract(
                html=detail_html,
                product_url=book.product_url,
                source_page=book.source_page,
                fetched_at=fetched_at
            )

            normalized_record = normalize_record(raw_record)
            validated_record = BookRecord.model_validate(normalized_record)

            valid_records.append(validated_record.model_dump(mode="json"))

        except (ValueError, ValidationError) as e:
            errors.append(
                {
                    "product_url": book.product_url,
                    "reason": str(e),
                }
            )

    write_json(
        OUTPUT_DIR / "books.json",
        valid_records,
    )

    write_json(
        OUTPUT_DIR / "errors.json",
        errors,
    )

    print(f"catalogue_pages={result.catalogue_pages}")
    print(f"discovered={len(result.discovered_books)}")
    print(f"unique_urls={len(unique_books)}")
    print(f"valid_records={len(valid_records)}")
    print(f"validation_errors={len(errors)}")   

if __name__ == "__main__":
    main()