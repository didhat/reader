from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from src.infrastructure.db.tables.book import book_table


class BookFilter(Filter):
    chapter_number__gte: Optional[int] = None
    chapter_number__lte: Optional[int] = None

    class Constants(Filter.Constants):
        model = book_table.c  # type: ignore
