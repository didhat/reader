import pathlib

from src.application import dto


class BookCoverRepository:
    def __init__(self, path: pathlib.Path):
        self._cover_folder = path

    async def get_cover_file(self, book_id: str) -> dto.BookCoverFile | None:
        file_path, fmt = self._get_file_path_with_cover(book_id)
        if file_path is None or fmt is None:
            return None

        return dto.BookCoverFile(file=file_path.read_bytes(), format=fmt)

    async def upload_book_cover(self, cover: dto.BookCoverFile, book_id: str):
        file_path = self._cover_folder / f"{book_id}.{cover.format}"
        file_path.write_bytes(cover.file)

    def _get_file_path_with_cover(
        self, book_id
    ) -> tuple[pathlib.Path, dto.CoverFormat] | tuple[None, None]:
        for fmt in dto.CoverFormat:
            probably_file = self._cover_folder / f"{book_id}.{fmt}"
            if probably_file.exists():
                return probably_file, dto.CoverFormat[fmt]
        return None, None
