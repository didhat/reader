from sqlalchemy.ext.asyncio import AsyncSession

from typing import Callable


def book_info_repo_factory(session_factory: Callable[[], AsyncSession]):

    async def get_book_repo():
        async with session_factory() as session:
            pass

    return get_book_repo
