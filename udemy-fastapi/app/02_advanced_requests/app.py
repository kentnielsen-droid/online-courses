from fastapi import FastAPI, Path, Query, HTTPException
from .book import Book, BookRequest
from starlette import status

app = FastAPI()


BOOKS = [
    Book(
        1,
        "Computer Science Pro",
        "author one",
        "A cool book about Computer Science",
        5,
        20050601,
    ),
    Book(2, "Master FastAPI", "author two", "FastAPI master class", 4, 20090605),
    Book(
        3,
        "Python for Everyone!",
        "author three",
        "Beginner friendly Python book",
        3,
        20221125,
    ),
    Book(
        4,
        "Statistics in Medicine",
        "author two",
        "Using statistics in medicine industry",
        3,
        20151230,
    ),
    Book(5, "Worst Book", "author one", "A bad book", 1, 20010101),
    Book(6, "Average book", "author one", "Just another average book", 2, 20030202),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(404, f"The book with id {book_id} cannot be found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=-1, le=6)):
    books = []
    for book in BOOKS:
        if book.rating == book_rating:
            books.append(book)
    return books


@app.get("/books/publish_date/", status_code=status.HTTP_200_OK)
async def get_book_by_publish_date(publish_date: int = Query(ge=19000101)):
    books = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books.append(book)
    return books


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    isBookUpdated = False
    for i, book in enumerate(BOOKS):
        if book.id == BOOKS[i].id:
            BOOKS[i] = book
            isBookUpdated = True
    if not isBookUpdated:
        raise HTTPException(404, 'Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    isBookUpdated = False
    for i, book in enumerate(BOOKS):
        if book_id == BOOKS[i].id:
            del BOOKS[i]
            isBookUpdated = True
    if not isBookUpdated:
        raise HTTPException(404, 'Item not found')
