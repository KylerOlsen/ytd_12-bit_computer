# Kyler Olsen
# Feb 2024


class FileInfo:

    _filename: str
    _line: int
    _col: int
    _length: int
    _lines: int

    def __init__(
        self,
        filename: str,
        line: int,
        col: int,
        length: int,
        lines: int = 0,
    ):
        self._filename = filename
        self._line = line
        self._col = col
        self._length = length
        self._lines = lines

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"('{self._filename}',{self._line},{self._col},{self._length})"
        )

    def __add__(self, other: "FileInfo") -> "FileInfo":
        filename = self.filename
        line = self.line
        col = self.col
        if self.line != other.line:
            if other.lines == 0:
                length = other.col + other.length
            else:
                length = other.length
            lines = other.line - self.line
        else:
            length = (other.col + other.length) - col
            lines = 0
        return FileInfo(
            filename,
            line,
            col,
            length,
            lines,
        )

    @property
    def filename(self) -> str: return self._filename
    @property
    def line(self) -> int: return self._line
    @property
    def col(self) -> int: return self._col
    @property
    def length(self) -> int: return self._length
    @property
    def lines(self) -> int: return self._lines


class CompilerError(Exception):

    def __init__(self, message: str, file_info: FileInfo):
        new_message = message
        if file_info is not None:
            new_message += (
                f"\nIn file {file_info.filename} at line {file_info.line} "
            )
            if file_info.lines:
                new_message += f"to line {file_info.line + file_info.lines}"
                with open(file_info.filename, 'r') as file:
                    new_message += ''.join(
                        file.readlines()[
                            file_info.line-1:file_info.line + file_info.lines])
            else:
                new_message += f"col {file_info.col}\n\n"
                with open(file_info.filename, 'r') as file:
                    new_message += file.readlines()[file_info.line-1]
                new_message += ' ' * (
                    file_info.col - 1) + '^' * file_info.length

        super().__init__(new_message)
