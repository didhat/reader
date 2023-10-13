import asyncio

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.book_service import BookService
from src.presentation.providers.book_service import get_book_service
from src import get_root_path
from src.presentation.entrypoints.book import books
from src.infrastructure.di.factories import book_info_repo_factory, book_service_factory
from src.presentation.entrypoints.site.reader import reader


async def setup_app():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    book_folder = get_root_path() / "books"

    if not book_folder.exists():
        raise Exception("Book folder does not exist")

    books_file_repo = BookFileFSRepository(book_folder)

    _book_info_repo_factory = book_info_repo_factory()
    _book_service_factory = book_service_factory(
        books_file_repo, session_maker, _book_info_repo_factory
    )

    app = FastAPI()
    app.include_router(books)
    app.include_router(reader)

    app.dependency_overrides[get_book_service] = _book_service_factory

    return app


async def main():
    app = await setup_app()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
