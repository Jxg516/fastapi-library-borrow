from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Library L1 MVP", version="0.1.0")

_books: dict[int, dict] = {}
_next_id = 1


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    author: str = Field(min_length=1, max_length=80)


class BookOut(BookIn):
    id: int
    available: bool = True


class BorrowOut(BaseModel):
    book_id: int
    borrowed: bool


class ReturnOut(BaseModel):
    book_id: int
    returned: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books", response_model=list[BookOut])
def list_books():
    return list(_books.values())


@app.post("/books", response_model=BookOut, status_code=201)
def create_book(payload: BookIn):
    global _next_id
    book = BookOut(id=_next_id, **payload.model_dump())
    _books[_next_id] = book.model_dump()
    _next_id += 1
    return book


@app.post("/books/{book_id}/borrow", response_model=BorrowOut)
def borrow_book(book_id: int):
    book = _books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    if not book["available"]:
        raise HTTPException(status_code=409, detail="already borrowed")
    book["available"] = False
    return BorrowOut(book_id=book_id, borrowed=True)


@app.post("/books/{book_id}/return", response_model=ReturnOut)
def return_book(book_id: int):
    book = _books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    if book["available"]:
        raise HTTPException(status_code=409, detail="not borrowed")
    book["available"] = True
    return ReturnOut(book_id=book_id, returned=True)
