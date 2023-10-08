import asyncio

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.book_service import BookService
from src.presentation.providers.book_service import get_book_service
from src import get_root_path
from src.presentation.entrypoints.book import books

from pathlib import Path


async def setup_app():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")

    session_maker = async_sessionmaker(engine, expire_on_commit=False)


    book_folder = get_root_path() / "books"

    if not book_folder.exists():
        raise

    books_file_repo = BookFileFSRepository(book_folder)

    books_service = BookService(books_file_repo)

    app = FastAPI()
    app.include_router(books)

    app.dependency_overrides[get_book_service] = lambda: books_service

    return app


async def main():
    app = await setup_app()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
