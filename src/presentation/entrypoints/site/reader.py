from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.application.book_service import BookService
from src.presentation.providers.book_service import get_book_service

reader = APIRouter()
templates = Jinja2Templates(directory="webpack/dist")


@reader.get("/book/{book_id}/read/{chapter_number}", response_class=HTMLResponse)
async def get_book_read(
    request: Request,
    book_id: str,
    chapter_number: int,
    book_service: BookService = Depends(get_book_service),
):
    # chapter = await book_service.get_book_chapter(book_id, chapter_number)

    return templates.TemplateResponse("index.html", {"request": request})
