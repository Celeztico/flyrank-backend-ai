# Books to Scrape — Polite Scraper

A small production-style Python scraping pipeline built as part of the **FlyRank Backend Internship**.

The project demonstrates a polite and reproducible scraping workflow with HTTP fetching, caching, catalogue discovery, HTML extraction, normalization, validation, failure handling, and run reporting.

---

## Table of Contents

- [Overview](#overview)
- [Target Classification](#target-classification)
- [Scope](#scope)
- [Data Collected](#data-collected)
- [Project Architecture](#project-architecture)
- [Setup](#setup)
- [Running the Scraper](#running-the-scraper)
- [Pipeline](#pipeline)
- [Fetching and Caching](#fetching-and-caching)
- [Catalogue Discovery](#catalogue-discovery)
- [Raw Record Extraction](#raw-record-extraction)
- [Normalization and Validation](#normalization-and-validation)
- [Failure Handling](#failure-handling)
- [Run Reporting](#run-reporting)
- [Outputs](#outputs)
- [CSV Export](#csv-export)
- [Change Detection](#change-detection)
- [Politeness and Responsible Use](#politeness-and-responsible-use)
- [Project Structure](#project-structure)
- [Project Status](#project-status)
- [Evidence](#evidence)
- [License / Educational Use](#license--educational-use)

## Overview

This project implements a small production-style scraper for **Books to Scrape**, a website specifically intended as a practice environment for learning web scraping.

The scraper processes the first three catalogue pages, discovers the linked book detail pages, extracts structured information, validates the resulting records, and stores the final dataset as JSON.

The implementation emphasizes:

- polite HTTP requests
- local caching
- deterministic catalogue discovery
- targeted HTML extraction
- data normalization
- schema validation
- failure isolation
- reproducible output
- run-level reporting

---

## Target Classification

### Target

**Books to Scrape**

Books to Scrape is a public practice sandbox designed for learning and practising web scraping. It is therefore an appropriate target for this assignment.

### robots.txt

**Checked:** 2026-08-27

**Result:** No `robots.txt` file was found.

The result was recorded during target classification before implementing the scraper.

### Responsible Use

This project is intentionally limited to the Books to Scrape practice sandbox.

> I will not reuse this code on another site without checking its rules and terms first.

---

## Scope

The scraper processes **only the first three catalogue pages**.

Expected scope:

| Item             | Expected |
| ---------------- | -------: |
| Catalogue pages  |        3 |
| Books discovered |       60 |
| Unique book URLs |       60 |
| Detail pages     |       60 |

Book URLs are discovered from the catalogue pages rather than hardcoded.

---

## Data Collected

Each validated book record contains:

| Field               | Description                             |
| ------------------- | --------------------------------------- |
| `title`             | Book title                              |
| `product_url`       | Canonical product URL                   |
| `price_text`        | Original price text                     |
| `price_gbp`         | Numeric price in GBP                    |
| `availability_text` | Availability information                |
| `rating_text`       | Rating value                            |
| `description`       | Book description, or `null` when unavailable |
| `source_page`       | Catalogue page where the book was discovered |
| `fetched_at`        | Record processing timestamp             |

The original `price_text` is retained alongside the normalized numeric `price_gbp` value.

Missing descriptions are represented as `null`; the scraper does not invent missing data.

---

## Project Architecture

The scraper follows this pipeline:

```text
Books to Scrape
       │
       ▼
Fetch + Cache
       │
       ▼
Catalogue Discovery
       │
       ▼
Book Detail Extraction
       │
       ▼
Normalization
       │
       ▼
Pydantic Validation
       │
       ├──────────────► Validation Errors
       │
       ▼
Validated Records
       │
       ├──────────────► books.json
       ├──────────────► books.csv
       │
       ├──────────────► Change Detection
       │                       │
       │                       ▼
       │                  changes.json
       │
       └──────────────► Run Report
```

### Source Structure

```text
src/scraper/
├── cache.py
├── change_detection.py
├── config.py
├── discovery.py
├── extractor.py
├── fetcher.py
├── main.py
├── normalizer.py
├── reporting.py
├── schemas.py
└── storage.py
```

| Module                | Responsibility                                     |
| --------------------- | -------------------------------------------------- |
| `cache.py`            | Read and write cached HTML                         |
| `config.py`           | Project configuration                              |
| `fetcher.py`          | HTTP requests, delays, caching, and retry handling |
| `discovery.py`        | Catalogue pagination and book URL discovery        |
| `extractor.py`        | Extract raw fields from book detail pages          |
| `normalizer.py`       | Normalize prices, URLs, and text                   |
| `schemas.py`          | Pydantic data validation                           |
| `storage.py`          | JSON and CSV output                                |
| `reporting.py`        | Run-level reporting                                |
| `change_detection.py` | Compare datasets between runs                      |
| `main.py`             | Pipeline orchestration                             |

---

## Setup

### Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `pydantic`

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it before installing dependencies.

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Scraper

Run the scraper from the project root.

### PowerShell

```powershell
$env:PYTHONPATH="src"
python -m scraper.main
```

### Linux / macOS

```bash
PYTHONPATH=src python -m scraper.main
```

The scraper will:

1. discover the first three catalogue pages
2. discover the book URLs
3. fetch or load cached detail pages
4. extract raw records
5. normalize the records
6. validate them with Pydantic
7. write the validated dataset
8. produce a run report

---

## Pipeline

### 1. Fetch

The scraper starts from:

```text
https://books.toscrape.com/
```

The catalogue pages are fetched using the configured HTTP client and cached locally.

### 2. Discover

The scraper follows the site's own catalogue `next` links and stops after three catalogue pages.

### 3. Extract

Each discovered book URL is fetched and parsed using targeted Beautiful Soup selectors.

### 4. Normalize

Raw values are converted into the format required by the validated schema.

For example:

```text
£51.77
```

becomes:

```text
51.77
```

while the original:

```text
£51.77
```

is retained as `price_text`.

### 5. Validate

Each normalized record is validated against the Pydantic `BookRecord` schema.

### 6. Store

Validated records are written to the output dataset.

### 7. Report

The run produces metrics covering the number of pages processed, cache hits, valid records, validation errors, failed pages, and execution time.

---

## Fetching and Caching

The scraper uses Python Requests for HTTP fetching.

Each real request:

- uses an identifying User-Agent
- has a 10-second timeout
- checks the HTTP status before accepting the response
- is separated from the previous real request by at least 500 ms

Successful HTML responses are stored in:

```text
cache/
```

Cached responses are reused on subsequent runs, avoiding unnecessary requests to the target website.

A second development run therefore primarily produces `CACHE HIT` messages rather than making the same HTTP requests again.

---

## Catalogue Discovery

The scraper starts from the main Books to Scrape catalogue and follows the catalogue's own `next` links.

Only the first three catalogue pages are processed.

Book links are extracted from the product listing area and converted from relative URLs to absolute URLs using Python's `urljoin()`.

Duplicate product URLs are removed before detail-page processing.

Expected discovery result:

```text
catalogue_pages=3
discovered=60
unique_urls=60
```

---

## Raw Record Extraction

For every discovered book, the detail page is parsed using targeted selectors around the product information.

The raw extraction stage produces:

```text
title
product_url
price_text
availability_text
rating_text
description
source_page
fetched_at
```

The raw price remains text at this stage.

Descriptions that are unavailable are represented as `null` rather than being inferred or invented.

---

## Normalization and Validation

Before storage, raw records are normalized.

Normalization includes:

- converting `price_text` into numeric `price_gbp`
- ensuring URLs are absolute
- trimming textual fields
- preserving missing descriptions as `null`

Records are then validated using Pydantic.

The validated schema is defined in:

```text
src/scraper/schemas.py
```

### Valid Records

Written to:

```text
output/books.json
```

### Validation Errors

Written to:

```text
output/errors.json
```

Records are identified by their canonical product URL.

Each run rebuilds the output dataset rather than appending to the previous dataset, so rerunning the scraper does not produce duplicate records.

---

## Failure Handling

A failure on one page should not terminate the entire scraping run.

The scraper isolates individual page failures and continues processing the remaining pages.

### Retry Policy

| Failure              | Behavior                 |
| -------------------- | ------------------------ |
| Timeout              | Retry once               |
| HTTP 5xx             | Retry once               |
| HTTP 403             | No retry                 |
| HTTP 404             | No retry                 |
| Other request errors | Fail the individual page |

The scraper intentionally uses a simple retry policy for this assignment. It does not implement exponential backoff, jitter, or `Retry-After` handling.

### Failure Reporting

Failed pages are recorded in:

```text
output/run-report.json
```

Each failed page includes:

- URL
- failure reason
- whether the failure was retryable

### Deliberate Failure Test

A deliberately invalid Books to Scrape detail URL was used to verify failure isolation.

The expected behavior is:

```text
valid_records=60
validation_errors=0
failed_pages=1
```

The scraper completes the run and preserves the valid records while reporting the failed page separately.

---

## Run Reporting

Each run produces:

```text
output/run-report.json
```

The report contains:

- run start time
- run completion time
- duration
- catalogue pages processed
- detail pages attempted
- cache hits
- valid records
- validation errors
- failed pages

A successful normal run is expected to produce approximately:

```text
catalogue_pages=3
discovered=60
unique_urls=60
detail_pages=60
valid_records=60
validation_errors=0
failed_pages=0
```

---

## Outputs

The scraper produces the following artifacts:

```text
output/
├── books.json
├── books.csv
├── errors.json
└── run-report.json
```

### books.json

The primary validated dataset containing the scraped books.

### books.csv

A tabular representation of the validated dataset.

### errors.json

Validation and normalization failures encountered while processing records.

### run-report.json

Run-level execution and failure information.

---

## CSV Export

The validated records can also be exported to:

```text
output/books.csv
```

The CSV is generated from the validated records rather than independently scraping the website.

This ensures that the JSON and CSV outputs represent the same validated dataset.

CSV is a flat tabular format, so nested or structured values would need to be represented as scalar text. The current validated records contain only scalar fields and a nullable description, so no complex nested structures require special flattening.

---

## Change Detection

The scraper includes a simple dataset comparison mechanism.

Records are identified by their canonical `product_url`.

Two datasets can be compared to identify:

- `new` — records present only in the new dataset
- `changed` — records present in both datasets but with changed data
- `unchanged` — records present in both datasets with no relevant data changes
- `gone` — records present only in the previous dataset

The `fetched_at` timestamp is excluded from the comparison so that a normal subsequent run does not classify every record as changed solely because it was processed at a different time.

---

## Politeness and Responsible Use

This project is intentionally designed around a limited scraping target and conservative request behavior.

The scraper:

- identifies itself with a descriptive User-Agent
- uses request timeouts
- waits at least 500 ms between real requests
- caches successful responses
- avoids unnecessary repeat requests
- limits catalogue discovery to three pages
- does not hardcode the 60 book URLs
- checks the target's `robots.txt`
- handles failures without repeatedly requesting unavailable pages

This implementation is intended for the Books to Scrape practice environment.

Before adapting the scraper to another website, its `robots.txt`, terms, access restrictions, and applicable rules should be checked first.

> I will not reuse this code on another site without checking its rules and terms first.

---

## Project Structure

```text
A5_Polite_Scraper/
│
├── cache/
│
├── output/
│   ├── books.csv
│   ├── books.json
│   ├── errors.json
│   └── run-report.json
│
├── src/
│   └── scraper/
│       ├── __init__.py
│       ├── cache.py
│       ├── change_detection.py
│       ├── config.py
│       ├── discovery.py
│       ├── extractor.py
│       ├── fetcher.py
│       ├── main.py
│       ├── normalizer.py
│       ├── reporting.py
│       ├── schemas.py
│       └── storage.py
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## Project Status

### Core Assignment

- [x] Target classification
- [x] `robots.txt` check
- [x] Polite HTTP fetching
- [x] Local HTML caching
- [x] Three-page catalogue discovery
- [x] Detail-page extraction
- [x] Data normalization
- [x] Pydantic validation
- [x] JSON storage
- [x] Failure isolation
- [x] Retry handling
- [x] Run reporting
- [x] README and project evidence

### Additional Features

- [x] CSV export
- [x] Change detection

---

## Evidence

A normal cached run is expected to preserve the assignment's core dataset size:

```text
catalogue_pages=3
discovered=60
unique_urls=60
detail_pages=60
valid_records=60
validation_errors=0
failed_pages=0
```

A deliberate single-page failure should leave the valid dataset intact while reporting the failed page separately:

```text
valid_records=60
validation_errors=0
failed_pages=1
```

The generated `books.json` and `run-report.json` provide reproducible evidence of the scraper's output and execution behavior.

---

## License / Educational Use

This repository was created as an educational project for the FlyRank Backend Internship and is intended to demonstrate responsible scraping practices against a dedicated scraping practice sandbox.