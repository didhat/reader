from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.infrastructure.db.tables.book import book_table
from src.application import dto
from src.domain.book import Book


class BookDataRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_books_by_query(self, query: dto.BookQuery):
        req = (
            query.filter.filter(
                select(
                    book_table.c[
                        "id", "title", "author", "chapter_number", "added_time"
                    ]
                )
            )
            .offset(query.get_page_start())
            .limit(query.page_size)
        )

        cursor = await self._session.execute(req)

        books = cursor.all()

        result = []

        for raw in books:
            book_id, title, author, chapter_number, _ = raw
            result.append(
                Book(
                    book_id=book_id,
                    title=title,
                    author=author,
                    chapter_number=chapter_number,
                )
            )

        return result

    async def get_book_by_id(self, book_id: int) -> Book | None:
        cursor = await self._session.execute(
            select(
                book_table.c["id", "title", "author", "chapter_number", "added_time"]
            ).where(book_table.c.id == book_id)
        )

        raw = cursor.one_or_none()
        if raw is None:
            return None

        book_id, title, author, chapter_number, _ = raw

        return Book(
            book_id=book_id, title=title, author=author, chapter_number=chapter_number
        )

    async def add_book(self, book: dto.BookForUploadWithFileAndMetadataDTO) -> int:
        raw = await self._session.execute(
            insert(book_table)
            .values(
                {
                    "title": book.upload.book_title,
                    "author": book.upload.book_author,
                    "chapter_number": book.chapter_number,
                }
            )
            .returning(book_table.c.id)
        )
        (book_id,) = raw.one()
        await self._session.commit()

        return int(book_id)

    async def delete_book_by_id(self, book_id: int):
        await self._session.execute(
            book_table.delete().where(book_table.c.id == book_id)
        )
        await self._session.commit()
