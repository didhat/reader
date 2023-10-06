from ebooklib.epub import EpubItem, EpubHtml


class Chapter:
    def __init__(self, chapter: EpubItem):
        self._chapter = chapter

    def get_content(self):
        if isinstance(self._chapter, EpubHtml):
            return self._chapter.get_body_content().decode("utf-8")

        return self._chapter.get_content().decode("utf-8")
