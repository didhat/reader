from fastapi import Request
from pydantic import BaseModel

from src.domain.book import Book


class BookInfoResponse(BaseModel):
    title: str
    author: str
    book_id: int
    chapter_number: int

    @classmethod
    def from_book(cls, book: Book):
        return BookInfoResponse(
            title=book.title,
            author=book.author,
            book_id=book.book_id,
            chapter_number=book.chapter_number,
        )


class BookUploadedResponse(BaseModel):
    book_id: int


class BookInfoWithCoverResponse(BookInfoResponse):
    image_link: str

    @classmethod
    def from_book_with_link(cls, books: Book, request: Request):
        return BookInfoWithCoverResponse(
            title=books.title,
            author=books.author,
            book_id=books.book_id,
            chapter_number=books.chapter_number,
            image_link=str(request.url_for("get_book_cover", book_id=books.book_id)),
        )


class ManyBookResponse(BaseModel):
    books: list[BookInfoWithCoverResponse]

    @classmethod
    def from_books(cls, books: list[Book], request: Request):
        return ManyBookResponse(
            books=[
                BookInfoWithCoverResponse.from_book_with_link(b, request) for b in books
            ]
        )
