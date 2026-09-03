from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASE_URL = "https://books.toscrape.com/"

REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5

USER_AGENT = (
    "FlyRankInternshipScarper/1.0 "
    "(educational project; polite scraping)"
)

CACHE_DIR = PROJECT_ROOT / "cache"