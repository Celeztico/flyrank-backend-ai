from urllib.parse import urljoin, urlparse


def normalize_price(price_text: str) -> float:
    cleaned = price_text.strip().replace("Â£", "").replace(",", "")

    try:
        return float(cleaned)
    except ValueError as e:
        raise ValueError(f"Invalid price: {price_text}") from e


def normalize_url(url: str, base_url: str) -> str:
    absolute_url = urljoin(base_url, url)

    parsed = urlparse(absolute_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    return absolute_url

def normalize_record(raw_record: dict) -> dict:
    product_url = normalize_url(
        raw_record["product_url"],
        raw_record["source_page"],
    )

    source_page = normalize_url(
        raw_record["source_page"],
        raw_record["source_page"],
    )

    return {
        "title": raw_record["title"].strip(),
        "product_url": product_url,
        "price_text": raw_record["price_text"].strip(),
        "price_gbp": normalize_price(raw_record["price_text"]),
        "availability_text": raw_record["availability_text"].strip(),
        "rating_text": raw_record["rating_text"].strip(),
        "description": (
            raw_record["description"].strip()
            if raw_record["description"] is not None
            else None
        ),
        "source_page": source_page,
        "fetched_at": raw_record["fetched_at"],
    }