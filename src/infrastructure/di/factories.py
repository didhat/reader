from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.adapters.book_data_repo import BookDataRepository
from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.book_service import BookService


def book_info_repo_factory():
    def get_book_repo(session: AsyncSession):
        return BookDataRepository(session)

    return get_book_repo


def book_service_factory(
    book_file_repo: BookFileFSRepository,
    session_factory: Callable[[], AsyncSession],
    book_info_repo_factory: Callable[[AsyncSession], BookDataRepository],
):
    async def get_book_service():
        async with session_factory() as session:
            book_data_repo = book_info_repo_factory(session)
            book_service = BookService(book_file_repo, book_data_repo)
            yield book_service

    return get_book_service
