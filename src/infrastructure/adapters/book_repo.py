import shutil
from pathlib import Path
from tempfile import SpooledTemporaryFile

import ebooklib
from ebooklib import epub
from ebooklib.epub import EpubHtml
from ebooklib.utils import debug

from src.domain.book import EpubXBook
from src.infrastructure.epub.sorted import EpubBookWithMethods


class BookFileFSRepository:

    def __init__(self, book_folder: Path):
        self._book_folder = book_folder

    async def get_book(self, book_id: str) -> EpubXBook | None:
        file = self._book_folder / f"{book_id}.epub"

        if not file.exists():
            return None

        book = epub.read_epub(f"{self._book_folder.name}/{file.name}", {"ignore_ncx": True})

        return EpubXBook(EpubBookWithMethods(book))

    async def add_book_file(self, book_file: SpooledTemporaryFile, book_id: str):
        file_for_save = self._book_folder / f"{book_id}.epub"

        if file_for_save.exists():
            raise

        with file_for_save.open(mode="wb") as f:
            shutil.copyfileobj(book_file, f)

    async def delete_book_file(self, book_id: str):
        pass

# if __name__ == "__main__":
#     book = epub.read_epub("test2.epub", {"ignore_ncx": True})
#
#     chapters: list[EpubHtml] = list(book.get_items_of_type(9))
#     # content = chapters[5].get_body_content()
#     #
#     # debug(content.decode("utf-8"))
#     # print(chapters)
#
# # for item in book.get_items_of_type("CoverPage"):
# #     print(item)
# #
#     for item in book.get_items():
#         print(item)
