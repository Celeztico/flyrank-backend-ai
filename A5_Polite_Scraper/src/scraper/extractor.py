from bs4 import BeautifulSoup


class BookExtractor:
    def extract(
        self,
        html: str,
        product_url: str,
        source_page: str,
        fetched_at: str,
    ) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        product = soup.select_one("div.product_main")

        if product is None:
            raise ValueError("Product area not found")

        return {
            "title": self._extract_title(product),
            "product_url": product_url,
            "price_text": self._extract_price(product),
            "availability_text": self._extract_availability(product),
            "rating_text": self._extract_rating(product),
            "description": self._extract_description(soup),
            "source_page": source_page,
            "fetched_at": fetched_at,
        }

    def _extract_title(self, product: BeautifulSoup) -> str:
        title = product.select_one("h1")

        if title is None:
            raise ValueError("Title not found")

        return title.get_text(strip=True)

    def _extract_price(self, product: BeautifulSoup) -> str:
        price = product.select_one("p.price_color")

        if price is None:
            raise ValueError("Price not found")

        return price.get_text(strip=True)

    def _extract_availability(self, product: BeautifulSoup) -> str:
        availability = product.select_one("p.instock.availability")

        if availability is None:
            raise ValueError("Availability not found")

        return availability.get_text(" ", strip=True)

    def _extract_rating(self, product: BeautifulSoup) -> str:
        rating = product.select_one("p.star-rating")

        if rating is None:
            raise ValueError("Rating not found")

        classes = rating.get("class", [])

        rating_classes = {
            "One",
            "Two",
            "Three",
            "Four",
            "Five",
        }

        for value in classes:
            if value in rating_classes:
                return value

        raise ValueError("Rating value not found")

    def _extract_description(self, soup: BeautifulSoup) -> str | None:
        description_header = soup.select_one("#product_description")

        if description_header is None:
            return None

        description = description_header.find_next_sibling("p")

        if description is None:
            return None

        return description.get_text(" ", strip=True)