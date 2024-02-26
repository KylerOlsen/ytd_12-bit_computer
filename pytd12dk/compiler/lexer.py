# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import ClassVar, Sequence, TextIO

from .compiler_types import CompilerError, FileInfo


class _InterTokenType(Enum):
    Generic = 'Generic'
    Directive = 'Directive'
    SingleLineComment = 'SingleLineComment'
    MultiLineComment = 'MultiLineComment'
    Word = 'Word'
    NumberLiteral = 'NumberLiteral'
    CharLiteral = 'CharLiteral'
    StringLiteral = 'StringLiteral'
    Punctuation = 'Punctuation'


_OnlyNewLineTerminatedTokens = (
    _InterTokenType.Directive,
    _InterTokenType.SingleLineComment,
)

_NewLineTerminatedTokens = _OnlyNewLineTerminatedTokens + (
    _InterTokenType.Word,
    _InterTokenType.NumberLiteral,
    _InterTokenType.Punctuation,
)

_NewLineErrorTokens = (
    _InterTokenType.CharLiteral,
    _InterTokenType.StringLiteral,
)

_ID_Start = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz" "_"

_ID_Continue = _ID_Start + "0123456789"

_Keywords = (
    'struct',   'fn',   'enum',  'static',
    'if',       'else', 'do',    'while',
    'for',      'pub',  'let',   'break',
    'continue', 'True', 'False', 'None',
    'unsigned', 'int',  'fixed', 'float',
)

_Num_Start = "0123456789"

_Num_Second = _Num_Start + "box._Ee"

_Num_Continue = _Num_Start + "._" "ABCDEF" "abcdef"

_Punctuation_Any = "@$+-*/%~&|^<>=!?{}[]().->,;:"

_Punctuation = (
    "++",  "--",  "@",  "$",  "+",  "-",
    "*",   "/",   "%",  "~",  "&",  "|",
    "^",   "<<",  ">>", "=",  "+=", "-=",
    "*=",  "/=",  "%=", "&=", "|=", "^=",
    "<<=", ">>=", "!",  "&&", "||", "==",
    "!=",  "<",   "<=", ">",  ">=", "?",
    "{",   "}",   "[",  "]",  "(",  ")",
    ".",   "->",  ",",  ";",  ":",
)


class LexerError(CompilerError): pass


class Token:

    _type: ClassVar[str] = 'Generic'
    _value: str
    _file_info: FileInfo

    def __init__(self, value: str, file_info: FileInfo):
        self._value = value
        self._file_info = file_info

    @property
    def value(self) -> str: return self._value

    @property
    def file_info(self) -> FileInfo: return self._file_info

class Directive(Token): _type = 'Directive'
class Identifier(Token): _type = 'Identifier'
class Keyword(Token): _type = 'Keyword'
class NumberLiteral(Token): _type = 'NumberLiteral'
class CharLiteral(Token): _type = 'CharLiteral'
class StringLiteral(Token): _type = 'StringLiteral'
class Punctuation(Token): _type = 'Punctuation'


def lexer(file: str | TextIO, filename: str) -> Sequence[Token]:
    if not isinstance(file, str):
        file = file.read()
    tokens: list[Token] = []
    current: str = ""
    current_line: int = 0
    current_col: int = 0
    escaped: bool = False
    token_type: _InterTokenType = _InterTokenType.Generic

    for line, line_str in enumerate(file.splitlines()):
        if token_type in _NewLineErrorTokens:
            raise LexerError("Unexpected Newline")
        if token_type in _NewLineTerminatedTokens:
            fi = FileInfo(filename, current_line, current_col, len(current))
            if token_type is _InterTokenType.Directive:
                tokens.append(Directive(current, fi))
            elif token_type is _InterTokenType.Word:
                if len(current) > 15:
                    raise LexerError("Identifier Too Long")
                if current in _Keywords:
                    tokens.append(Keyword(current, fi))
                else:
                    tokens.append(Identifier(current, fi))
            elif token_type is _InterTokenType.NumberLiteral:
                tokens.append(NumberLiteral(current, fi))
            elif token_type is _InterTokenType.Punctuation:
                if current not in _Punctuation:
                    raise LexerError("Invalid Punctuation")
                tokens.append(Punctuation(current, fi))
            token_type = _InterTokenType.Generic

        for col, char in enumerate(line_str):
            if token_type in _OnlyNewLineTerminatedTokens:
                current += char
            elif token_type is _InterTokenType.MultiLineComment:
                if len(current) >= 2 and current[-1] == '*' and char == '/':
                    token_type = _InterTokenType.Generic
                    continue
                current += char
            elif token_type is _InterTokenType.Word:
                if char in _ID_Continue:
                    current += char
                else:
                    if len(current) > 15:
                        raise LexerError("Identifier Too Long")
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    if current in _Keywords:
                        tokens.append(Keyword(current, fi))
                    else:
                        tokens.append(Identifier(current, fi))
                token_type = _InterTokenType.Generic
            elif token_type is _InterTokenType.NumberLiteral:
                if (
                    (len(current) == 2 and char in _Num_Second) ^
                    (char in _Num_Continue)
                ):
                    current += char
                else:
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    tokens.append(NumberLiteral(current, fi))
                    token_type = _InterTokenType.Generic
            elif token_type is _InterTokenType.CharLiteral:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == "'":
                    current += char
                    if (
                        current[1] != '\\' and
                        len(current) == 3 or
                        len(current) > 3
                    ):
                        raise LexerError("Character Literal Too Long")
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    tokens.append(StringLiteral(current, fi))
                    token_type = _InterTokenType.Generic
                    continue
                current += char
            elif token_type is _InterTokenType.StringLiteral:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    current += char
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    tokens.append(StringLiteral(current, fi))
                    token_type = _InterTokenType.Generic
                    continue
                current += char
            elif token_type is _InterTokenType.Punctuation:
                if char in _Punctuation_Any:
                    current += char
                else:
                    if current not in _Punctuation:
                        raise LexerError("Invalid Punctuation")
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    tokens.append(Punctuation(current, fi))
                token_type = _InterTokenType.Generic

            if token_type is _InterTokenType.Generic:
                current = char
                current_line = line + 1
                current_col = col + 1
                escaped = False
                if char == '#': token_type = _InterTokenType.Directive
                elif char == '/' and line_str[col+1] == '/':
                    token_type = _InterTokenType.SingleLineComment
                elif char == '/' and line_str[col+1] == '*':
                    token_type = _InterTokenType.MultiLineComment
                elif char in _ID_Start:
                    token_type = _InterTokenType.Word
                elif char == '.' and line_str[col+1] in _Num_Second:
                    token_type = _InterTokenType.NumberLiteral
                elif char in _Num_Start:
                    token_type = _InterTokenType.NumberLiteral
                elif char == "'":
                    token_type = _InterTokenType.CharLiteral
                elif char == '"':
                    token_type = _InterTokenType.StringLiteral
                elif char in _Punctuation_Any:
                    token_type = _InterTokenType.Punctuation

    return tokens
