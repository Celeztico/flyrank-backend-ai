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