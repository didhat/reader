from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.infrastructure.db.tables.base import meta


book_table = Table(
    "book",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(100)),
    Column("author", String(100)),
    Column("chapter_number", Integer),
    Column("added_time", DateTime, server_default=func.now()),
)
