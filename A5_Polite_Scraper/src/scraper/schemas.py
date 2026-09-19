from pydantic import BaseModel, Field, HttpUrl

class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float = Field(ge=0)
    availability_text: str
    rating_text: str
    description: str | None
    source_page: HttpUrl
    fetched_at: str