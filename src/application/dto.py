import attrs

from tempfile import SpooledTemporaryFile

from src.domain.chapter import Chapter


@attrs.define
class ChapterHtmlFileDTO:
    content: str

    @classmethod
    def from_chapter(cls, chapter: Chapter):
        content = chapter.get_content()

        return cls(content=content)


@attrs.define
class BookForUploadDTO:
    format: str
    book_title: str
    book_author: str


@attrs.define
class BookForUploadWithFileDTO(BookForUploadDTO):
    file: SpooledTemporaryFile
    filename: str


@attrs.define
class BookForUploadWithFileAndMetadataDTO:
    upload: BookForUploadWithFileDTO
    chapter_number: int
