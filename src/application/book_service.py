from src.infrastructure.adapters.book_repo import BookFileFSRepository
from src.application.exceptions import BookNotFound, ChapterNotFound
from src.application import dto
from src.infrastructure.adapters.book_data_repo import BookDataRepository


class BookService:
    def __init__(self, book_file_repo: BookFileFSRepository, book_data_repo: BookDataRepository):
        self._book_file_repository = book_file_repo
        self._book_data_repo = book_data_repo

    async def get_book_by_id(self, book_id: int):
        book = await self._book_data_repo.get_book_by_id(book_id)
        if book is None:
            raise BookNotFound()

        return book

    async def get_book_chapter(self, book_id: str, chapter_number):
        book = await self._book_file_repository.get_book(book_id)

        if book is None:
            raise BookNotFound()

        chapter = book.get_chapter(chapter_number)

        if chapter is None:
            raise ChapterNotFound()

        return dto.ChapterHtmlFileDTO.from_chapter(chapter)

    async def upload_book(self, upload: dto.BookForUploadWithFileDTO):
        await self._book_file_repository.add_book_file(upload.file, upload.book_title)

    async def delete_book(self, book_id: str):
        await self._book_file_repository.delete_book_file(book_id)
