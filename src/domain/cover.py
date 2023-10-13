import attrs


@attrs.define
class BookCover:
    file: bytes
    format: str
