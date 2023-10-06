import ebooklib

from src.infrastructure.epub.sorted import EpubBookWithMethods
from src.domain.chapter import Chapter


class EpubXBook:

    def __init__(self, book: EpubBookWithMethods):
        self._book = book

    def get_chapters(self):
        chapters = [Chapter(ch) for ch in self._book.get_chapters_in_order()]

        return chapters

    def get_chapter(self, ch_number: int):
        pass

