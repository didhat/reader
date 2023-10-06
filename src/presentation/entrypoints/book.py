from fastapi import APIRouter, Depends
from src.presentation.providers.book_service import get_book_service
from src.application.book_service import BookService
from src.presentation.webmodels.chapter import ChapterResponse

books = APIRouter()


@books.get("/books/{book_id}/chapters/{chapter_id}")
async def get_book_chapter(book_id: str, chapter_id: int, book_service: BookService = Depends(get_book_service)) -> ChapterResponse:
    chapter = await book_service.get_book_chapter(book_id, chapter_id)

    return ChapterResponse.from_chapter_dto(chapter)
