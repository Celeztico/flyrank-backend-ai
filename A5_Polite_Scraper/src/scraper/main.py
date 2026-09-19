import time
from scraper.fetcher import Fetcher, FetchError
from scraper.discovery import CatalogueDiscovery
from scraper.extractor import BookExtractor
from scraper.normalizer import normalize_record
from scraper.reporting import create_run_report
from scraper.schemas import BookRecord
from scraper.storage import write_json
from scraper.config import BASE_URL, OUTPUT_DIR
from datetime import datetime, timezone
from pydantic import ValidationError

def main():
    start_time = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()

    fetcher = Fetcher()
    discovery = CatalogueDiscovery(fetcher)
    extractor = BookExtractor()

    result = discovery.discover(BASE_URL, max_pages=3)
    unique_books = result.unique_books

    valid_records = []
    errors = []
    failed_pages = []

    detail_pages = 0

    for book in unique_books:
        detail_pages += 1
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

        except FetchError as e:
            failed_pages.append(
                {
                    "url": book.product_url,
                    "reason": str(e),
                    "retryable": e.retryable,
                }
            )

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

    finished_at = datetime.now(timezone.utc).isoformat()
    duration_seconds = (time.monotonic() - start_time)

    report = create_run_report(
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=duration_seconds,
        catalogue_pages=result.catalogue_pages,
        detail_pages=detail_pages,
        cache_hits=fetcher.cache_hits,
        valid_records=len(valid_records),
        validation_errors=len(errors),
        failed_pages=failed_pages,
    )

    write_json(OUTPUT_DIR / "run-report.json", report)

    print(f"catalogue_pages={result.catalogue_pages}")
    print(f"discovered={len(result.discovered_books)}")
    print(f"unique_urls={len(unique_books)}")
    print(f"detail_pages={detail_pages}")
    print(f"cache_hits={fetcher.cache_hits}")
    print(f"valid_records={len(valid_records)}")
    print(f"validation_errors={len(errors)}")   
    print(f"failed_pages={len(failed_pages)}")

if __name__ == "__main__":
    main()