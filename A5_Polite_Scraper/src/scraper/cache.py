import hashlib
from pathlib import Path

def cache_path(cache_dir: Path, url: str) -> Path:
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return cache_dir / f"{url_hash}.html"

def read_cache(cache_dir: Path, url: str) -> str | None:
    path = cache_path(cache_dir, url)

    if not path.exists():
        return None

    return path.read_text(encoding="utf-8")

def write_cache(cache_dir: Path, url: str, content: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)

    path = cache_path(cache_dir, url)
    path.write_text(content, encoding="utf-8")

    return path