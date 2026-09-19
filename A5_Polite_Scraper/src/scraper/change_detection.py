from typing import Any


def index_by_url(records: list[dict]) -> dict[str, dict]:
    return {
        record["product_url"]: record
        for record in records
    }

def comparable_record(record: dict) -> dict:
    return {
        key: value
        for key, value in record.items()
        if key != "fetched_at"
    }


def compare_records(
    previous: list[dict],
    current: list[dict],
) -> dict[str, list[dict]]:
    previous_by_url = index_by_url(previous)
    current_by_url = index_by_url(current)

    new = []
    changed = []
    unchanged = []
    gone = []

    for url, current_record in current_by_url.items():
        if url not in previous_by_url:
            new.append(current_record)
            continue

        previous_record = previous_by_url[url]

        if comparable_record(current_record) == comparable_record(previous_record):
            unchanged.append(current_record)
        else:
            changed.append(
                {
                    "product_url": url,
                    "previous": previous_record,
                    "current": current_record,
                }
            )

    for url, previous_record in previous_by_url.items():
        if url not in current_by_url:
            gone.append(previous_record)

    return {
        "new": new,
        "changed": changed,
        "unchanged": unchanged,
        "gone": gone,
    }