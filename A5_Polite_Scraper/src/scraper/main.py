from scraper.fetcher import Fetcher
from scraper.config import BASE_URL

def main():
    fetcher = Fetcher()

    fetcher.fetch(BASE_URL)

if __name__ == "__main__":
    main()