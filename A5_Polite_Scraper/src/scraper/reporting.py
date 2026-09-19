def create_run_report(
    *,
    started_at: str,
    finished_at: str,
    duration_seconds: float,
    catalogue_pages: int,
    detail_pages: int,
    cache_hits: int,
    valid_records: int,
    validation_errors: int,
    failed_pages: list[dict],
) -> dict:
    return {
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_seconds": round(duration_seconds, 3),
        "catalogue_pages": catalogue_pages,
        "detail_pages": detail_pages,
        "cache_hits": cache_hits,
        "valid_records": valid_records,
        "validation_errors": validation_errors,
        "failed_pages": failed_pages,
    }