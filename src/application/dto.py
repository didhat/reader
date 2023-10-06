import attrs

from src.domain.chapter import Chapter


@attrs.define
class ChapterHtmlFileDTO:
    content: str

    @classmethod
    def from_chapter(cls, chapter: Chapter):
        content = chapter.get_content()

        return cls(content=content)