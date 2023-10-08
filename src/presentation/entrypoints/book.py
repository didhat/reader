from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Form
from fastapi.datastructures import FormData

from src.presentation.providers.book_service import get_book_service
from src.application.book_service import BookService
from src.presentation.webmodels.chapter import ChapterResponse
from src.presentation.webmodels.book import BookInfoResponse
from src.application import dto

books = APIRouter()


@books.get("/books/{book_id}/chapters/{chapter_id}")
async def get_book_chapter(book_id: str, chapter_id: int,
                           book_service: BookService = Depends(get_book_service)) -> ChapterResponse:
    chapter = await book_service.get_book_chapter(book_id, chapter_id)

    return ChapterResponse.from_chapter_dto(chapter)


@books.post("/books/upload")
async def upload_book(book_file: Annotated[UploadFile, Form()], title: Annotated[str | None, Form()],
                      author: Annotated[str | None, Form()], book_service: BookService = Depends(get_book_service)):
    upload = dto.BookForUploadWithFileDTO(file=book_file.file, filename=book_file.filename,
                                          format=book_file.content_type,
                                          book_title=title, book_author=author)

    await book_service.upload_book(upload)


@books.delete("/books/{book_id}")
async def delete_book(book_id: str, book_service: BookService = Depends(get_book_service)):
    await book_service.delete_book(book_id)


@books.get("/books/{book_id}")
async def get_book_info(book_id: int, book_service: BookService = Depends(get_book_service)) -> BookInfoResponse:
    book = await book_service.get_book_by_id(book_id)

    return BookInfoResponse.from_book(book)
