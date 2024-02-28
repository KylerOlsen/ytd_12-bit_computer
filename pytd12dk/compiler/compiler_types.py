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


class CompilerError(Exception):

    def __init__(self, message: str, file_info: FileInfo):
        super().__init__(message, file_info)
