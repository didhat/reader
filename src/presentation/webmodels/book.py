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