from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.adapters.book_data_repo import BookDataRepository
from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.book_service import BookService


def book_info_repo_factory(session_factory: Callable[[], AsyncSession]):
    async def get_book_repo():
        async with session_factory() as session:
            return BookDataRepository(session)

    return get_book_repo


def book_service_factory(book_file_repo: BookFileFSRepository,
                         book_info_repo_factory: Callable[[], BookDataRepository]):
    async def get_book_service():
        book_info_repo = await book_info_repo_factory()

        book_service = BookService(book_file_repo, book_info_repo)

        return book_service

    return get_book_service
