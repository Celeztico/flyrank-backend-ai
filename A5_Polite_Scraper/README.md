# Books to Scrape — Polite Scraper

A small Python scraping pipeline built as part of the FlyRank Backend Internship.

## Target classification

### Target

[Books to Scrape](https://books.toscrape.com/)

Books to Scrape is a public practice sandbox designed for learning and
practising web scraping. It is therefore an appropriate target for this
assignment.

### Scope

The scraper will process only the first three catalogue pages.

The expected scope is:

- 3 catalogue pages
- approximately 60 books
- book detail pages linked from those catalogue pages

The scraper will discover the book URLs from the catalogue pages rather
than hardcoding the 60 URLs.

### Data collected

For each book, the scraper will collect:

- title
- product URL
- price
- availability
- rating
- description
- source catalogue page
- fetch timestamp

The raw price will later be normalized into a numeric `price_gbp` value.

### robots.txt

Checked on: 2026-08-27

Result:

no robots file found

The robots.txt result is recorded here as part of the target classification
before implementing the scraper.

### Responsible use

This project is intentionally limited to the public Books to Scrape
practice sandbox.

I will not reuse this code on another site without checking its rules and terms first.

## Fetching and caching

The scraper uses Python Requests for HTTP fetching.

Each real request:

- uses an identifying User-Agent
- has a 10-second timeout
- checks the HTTP status before accepting the response
- is separated from the previous real request by at least 500 ms

Successful HTML responses are cached locally in `cache/`.

Cached responses are reused on subsequent runs, avoiding unnecessary
requests to the target website.

## Catalogue discovery

The scraper starts from the Books to Scrape catalogue and follows the
catalogue's own `next` links.

Only the first three catalogue pages are processed, matching the assignment
scope.

Book links are extracted from the product listing area and converted from
relative URLs to absolute URLs using Python's `urljoin()`.

Duplicate product URLs are removed before the detail-page extraction stage.

The expected discovery result is:

- catalogue pages: 3
- discovered book URLs: 60
- unique book URLs: 60

## Raw record extraction

For each discovered book URL, the scraper fetches the detail page using the
same HTTP politeness rules as the catalogue pages.

Each raw record contains:

- `title`
- `product_url`
- `price_text`
- `availability_text`
- `rating_text`
- `description`
- `source_page`
- `fetched_at`

The raw price is intentionally retained as text at this stage. Numeric price
normalization is performed during the validation/storage stage.

Missing descriptions are represented as `null` rather than being inferred or
invented.

Detail pages are cached locally so subsequent development runs do not need to
request the same pages again.

## Normalization and validation

Raw extracted records are normalized before storage.

Normalization includes:

- converting `price_text` such as `£51.77` into numeric `price_gbp`
- ensuring URLs are absolute
- trimming textual fields
- preserving missing descriptions as `null`

Normalized records are validated using Pydantic.

Valid records are written to:

`output/books.json`

Validation failures are written to:

`output/errors.json`

Records are identified by their canonical product URL, and each run
rebuilds the output dataset rather than appending duplicate records.

## Failure handling and run reporting

The scraper isolates failures at the individual page level so that one
unavailable detail page does not terminate the entire run.

Timeouts and HTTP 5xx responses are retried once.

HTTP 403 and 404 responses are not retried.

A failed page is recorded in `output/run-report.json` with its URL,
failure reason, and whether the failure was retryable.

Each run reports:

- catalogue pages processed
- detail pages attempted
- cache hits
- valid records
- validation errors
- failed pages
- run start/end timestamps
- duration

### Failure test

A deliberately invalid Books to Scrape URL was used to verify that a single
failed detail page does not terminate the scraper.

The run completed with the remaining records intact and reported the failed
page separately in `run-report.json`.