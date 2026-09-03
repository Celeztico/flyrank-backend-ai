from scraper.fetcher import Fetcher
from scraper.discovery import CatalogueDiscovery
from scraper.config import BASE_URL

def main():
    fetcher = Fetcher()
    discovery = CatalogueDiscovery(fetcher)

    result = discovery.discover(BASE_URL, max_pages=3)

    print(f"catalogue_pages={result.catalogue_pages}")
    print(f"discovered={len(result.discovered_urls)}")
    print(f"unique_urls={len(result.unique_urls)}")

if __name__ == "__main__":
    main()