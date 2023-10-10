import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, insert

from src.infrastructure.db.tables.book import book_table
from src.application import dto
from src.domain.book import Book


class BookDataRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_book_by_id(self, book_id: int) -> Book | None:
        cursor = await self._session.execute(
            select(
                book_table.c["id", "title", "author", "chapter_number", "added_time"]
            ).where(book_table.c.id == book_id)
        )

        raw = cursor.one_or_none()
        if raw is None:
            return None

        book_id, title, author, _, _ = raw

        return Book(book_id=book_id, title=title, author=author)

    async def add_book(self, book: dto.BookForUploadDTO) -> int:
        raw = await self._session.execute(
            insert(book_table)
            .values(
                {
                    "title": book.book_title,
                    "author": book.book_author,
                    "chapter_number": 1,
                }
            )
            .returning(book_table.c.id)
        )
        book_id, = raw.one()
        await self._session.commit()

        return int(book_id)

    async def delete_book_by_id(self, book_id: int):
        await self._session.execute(
            book_table.delete().where(book_table.c.id == book_id)
        )
        await self._session.commit()
