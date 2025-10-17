from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Three", "category": "math"},
    {"title": "Title Five", "author": "Author Two", "category": "math"},
    {"title": "Title Six", "author": "Author One", "category": "chemestry"},
    {"title": "Title Seven", "author": "Author One", "category": "medicine"},
]


# GET REQUEST METHODS
@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/books")
async def books():
    return BOOKS


@app.get("/books/mybook")
async def books():  # <- This is called instead of the other books functions with parameters if param is "mybook"
    book = BOOKS[0]
    return book


@app.get("/books/{book_title}")
async def books(
    book_title: str,
):  # <- If book_title = mybook, the previous function (books()) is called instead due to fastapi looking chronologically.
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def books_by_category(category: str):
    books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/books/{book_author}/")
async def books_by_category(book_author: str, category: str):
    books = []
    for book in BOOKS:
        if (
            book.get("category").casefold() == category.casefold()
            and book.get("author").casefold() == book_author.casefold()
        ):
            books.append(book)
    return books


@app.get("/books/author/{book_author}")
async def books_by_author(book_author: str):
    books = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books.append(book)
    return books


# POST REQUEST METHODS
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# PUT REQUEST METHODS
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = update_book


# DELETE REQUEST METHODS
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == book_title.casefold():
            del BOOKS[i]  # BOOKS.pop(i)
