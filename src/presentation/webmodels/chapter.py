from pydantic import BaseModel

from src.application import dto


class ChapterResponse(BaseModel):
    content: str

    @classmethod
    def from_chapter_dto(cls, chapter: dto.ChapterHtmlFileDTO):
        return ChapterResponse(content=chapter.content)
