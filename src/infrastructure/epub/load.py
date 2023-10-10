import zipfile
from tempfile import SpooledTemporaryFile
from ebooklib import epub

from src.infrastructure.epub.sorted import EpubBookWithMethods


def load_epub_from_upload(file: SpooledTemporaryFile, filename: str):
    file = zipfile.ZipFile(file, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True)

    reader = epub.EpubReader(filename, {"ignore_ncx": True})
    reader.zf = file
    reader._load_container()
    reader._load_opf_file()

    file.close()

    book = reader.book

    reader.process()

    return EpubBookWithMethods(book)
