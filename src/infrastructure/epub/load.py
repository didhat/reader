import shutil

import zipfile
from tempfile import SpooledTemporaryFile
from ebooklib import epub

from src.infrastructure.epub.sorted import EpubBookWithMethods


def load_epub_from_upload(file: SpooledTemporaryFile, filename: str):
    reader = EpubBookWithUploadFromBinary.from_binary(file, filename)

    book = reader.book
    reader.process()

    return EpubBookWithMethods(book)


class EpubBookWithUploadFromBinary(epub.EpubReader):
    @classmethod
    def from_binary(cls, file: SpooledTemporaryFile, filename: str):
        file_copy = create_file_deepcopy(file)
        reader = cls(filename, {"ignore_ncx": True})

        zip_file = zipfile.ZipFile(
            file_copy, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True
        )

        reader.zf = zip_file

        reader._load_container()
        reader._load_opf_file()

        zip_file.close()
        file_copy.close()

        return reader


def create_file_deepcopy(file: SpooledTemporaryFile):
    file_copy = SpooledTemporaryFile(mode="wb+")
    shutil.copyfileobj(file, file_copy)
    file_copy.seek(0)
    file.seek(0)
    return file_copy
