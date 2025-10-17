from pydantic import BaseModel, Field
from typing import Optional


class Book:
    id: int
    title: str
    author: str
    desciption: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.desciption = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(min_length=8, max_length=8, ge=19000101)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "author name",
                "description": "Description of book",
                "rating": 5,
                "published_date": 20250101
            }
        }
    }