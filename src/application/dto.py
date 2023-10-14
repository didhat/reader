import enum
from tempfile import SpooledTemporaryFile

import attrs

from src.domain.chapter import Chapter
from src.presentation.filters.book import BookFilter


@attrs.define
class ChapterHtmlFileDTO:
    content: str

    @classmethod
    def from_chapter(cls, chapter: Chapter):
        content = chapter.get_content()

        return cls(content=content)


@attrs.define
class BookForUploadDTO:
    format: str | None
    book_title: str | None
    book_author: str | None


@attrs.define
class BookForUploadWithFileDTO(BookForUploadDTO):
    file: SpooledTemporaryFile
    filename: str | None


@attrs.define
class BookForUploadWithFileAndMetadataDTO:
    upload: BookForUploadWithFileDTO
    chapter_number: int


@attrs.define
class BookQuery:
    page: int
    page_size: int
    filter: BookFilter

    def get_page_start(self):
        return self.page * self.page_size


class CoverFormat(enum.StrEnum):
    png = "png"
    jpeg = "jpeg"
    jpg = "jpg"


@attrs.define
class BookCoverFile:
    file: bytes
    format: str
