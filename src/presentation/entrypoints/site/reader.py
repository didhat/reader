from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.presentation.entrypoints.site.utils import escapejs, compact_json

reader = APIRouter()
templates = Jinja2Templates(directory="webui/dist")


@reader.get("/site", response_class=HTMLResponse)
async def get_book_read(
    request: Request,
):
    ui_data = {"books": str(request.url_for("get_books"))}

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "preload_safe": escapejs(compact_json(ui_data))},
    )
