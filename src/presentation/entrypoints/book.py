from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Form, Response, Request
from fastapi.datastructures import FormData
from fastapi_filter import FilterDepends

from src.presentation.filters.book import BookFilter
from src.presentation.providers.book_service import get_book_service
from src.application.book_service import BookService
from src.presentation.webmodels.chapter import ChapterResponse
from src.presentation.webmodels.book import (
    BookInfoResponse,
    BookInfoWithCoverResponse,
    BookUploadedResponse,
    ManyBookResponse,
)
from src.application import dto

books = APIRouter()


@books.get("/books/{book_id}/chapters/{chapter_id}")
async def get_book_chapter(
    book_id: str, chapter_id: int, book_service: BookService = Depends(get_book_service)
) -> ChapterResponse:
    chapter = await book_service.get_book_chapter(book_id, chapter_id)

    return ChapterResponse.from_chapter_dto(chapter)


@books.post("/books/upload")
async def upload_book(
    book_file: Annotated[UploadFile, Form()],
    title: Annotated[str | None, Form()],
    author: Annotated[str | None, Form()],
    book_service: BookService = Depends(get_book_service),
) -> BookUploadedResponse:
    upload = dto.BookForUploadWithFileDTO(
        file=book_file.file,
        filename=book_file.filename,
        format=book_file.content_type,
        book_title=title,
        book_author=author,
    )

    book_id = await book_service.upload_book(upload)

    return BookUploadedResponse(book_id=book_id)


@books.delete("/books/{book_id}")
async def delete_book(
    book_id: int, book_service: BookService = Depends(get_book_service)
):
    await book_service.delete_book(book_id)


@books.get("/books/{book_id}")
async def get_book_info(
    request: Request,
    book_id: int,
    book_service: BookService = Depends(get_book_service),
) -> BookInfoWithCoverResponse:
    book = await book_service.get_book_by_id(book_id)

    return BookInfoWithCoverResponse.from_book_with_link(book, request)


@books.get("/books")
async def get_books(
    request: Request,
    page: int,
    page_size: int,
    book_filter: BookFilter = FilterDepends(BookFilter),
    book_service: BookService = Depends(get_book_service),
):
    user_books = await book_service.get_books(
        dto.BookQuery(page=page, page_size=page_size, filter=book_filter)
    )

    return ManyBookResponse.from_books(user_books, request)


@books.get("/books/{book_id}/cover")
async def get_book_cover(
    book_id: str, book_service: BookService = Depends(get_book_service)
):
    cover = await book_service.get_book_cover(book_id)

    return Response(content=cover.file, media_type=f"image/{cover.format}")
