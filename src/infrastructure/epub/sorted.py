import ebooklib
from ebooklib.epub import EpubBook, EpubItem

from src.domain.cover import BookCover


class EpubBookWithMethods:
    def __init__(self, book: EpubBook):
        self._book = book
        self._chapters = self._get_chapters_in_order()

    def get_title(self):
        return self._book.metadata.get("DC", "title")

    def get_author(self):
        return self._book.metadata.get("DC", "creator")

    def get_cover(self) -> BookCover | None:
        cover = list(self._book.get_items_of_type(ebooklib.ITEM_IMAGE))

        if not cover:
            return None

        file = cover[0].get_content()
        file_format = cover[0].get_name().split(".")[-1]

        return BookCover(file=file, format=file_format)

    def get_chapters_in_order(self) -> list[EpubItem]:
        return self._chapters

    def get_chapter_by_number(self, number: int) -> EpubItem | None:
        if number - 1 > len(self._chapters) or number <= 0:
            return None

        return self._chapters[number - 1]

    def _get_item_by_id(self, item_id: str):
        for item in self._book.items:
            if item.id == item_id:
                return item

    def _get_chapters_in_order(self):
        chapter_order = self._book.spine
        return [
            self._get_item_by_id(ch_id)
            for ch_id, status in chapter_order
            if status == "yes"
        ]
