# Kyler Olsen
# Feb 2024


class FileInfo:

    _filename: str
    _line: int
    _col: int
    _length: int

    def __init__(
        self,
        filename: str,
        line: int,
        col: int,
        length: int,
    ):
        self._filename = filename
        self._line = line
        self._col = col
        self._length = length

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"('{self._filename}',{self._line},{self._col},{self._length})"
        )


class CompilerError(Exception):

    def __init__(self, message: str, file_info: FileInfo):
        super().__init__(message, file_info)
