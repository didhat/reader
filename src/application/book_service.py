from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.exceptions import BookNotFound, ChapterNotFound
from src.application import dto


class BookService:
    def __init__(self, book_file_repo: BookFileFSRepository):
        self._book_file_repository = book_file_repo

    async def get_book_chapter(self, book_id: str, chapter_number):
        book = await self._book_file_repository.get_book(book_id)

        if book is None:
            raise BookNotFound()

        chapter = book.get_chapter(chapter_number)

        if chapter is None:
            raise ChapterNotFound()

        return dto.ChapterHtmlFileDTO.from_chapter(chapter)


