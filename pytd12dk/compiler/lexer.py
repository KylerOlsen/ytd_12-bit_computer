# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import ClassVar, Sequence

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


class _NumberLiteralType(Enum):
    Number = 'Number'
    Real = 'Real'
    Exp = 'Exp'
    Base = 'Base'
    Binary = 'Binary'
    Octal = 'Octal'
    Hex = 'Hex'


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
    'struct',   'fn',    'enum',  'static',
    'if',       'else',  'do',    'while',
    'for',      'let',   'break', 'continue',
    'unsigned', 'int',   'fixed', 'float',
    'True',     'False', 'None',
)

_Num_Start = "0123456789"

_Num_Start_Next = {
    _NumberLiteralType.Number: {
        '.': _NumberLiteralType.Real,
        '0': _NumberLiteralType.Base,
    }
}

_Num_Second = {
    _NumberLiteralType.Number: _Num_Start + ".eE_",
    _NumberLiteralType.Real: _Num_Start + "eE_",
    _NumberLiteralType.Base: "bBoOxX",
}

_Num_Second_Next = {
    _NumberLiteralType.Number: {
        '.': _NumberLiteralType.Real,
        'e': _NumberLiteralType.Exp,
        'E': _NumberLiteralType.Exp,
    },
    _NumberLiteralType.Real: {
        'e': _NumberLiteralType.Exp,
        'E': _NumberLiteralType.Exp,
    },
    _NumberLiteralType.Base: {
        'b': _NumberLiteralType.Binary,
        'B': _NumberLiteralType.Binary,
        'o': _NumberLiteralType.Octal,
        'O': _NumberLiteralType.Octal,
        'x': _NumberLiteralType.Hex,
        'X': _NumberLiteralType.Hex,
    }
}

_Num_Continue = {
    _NumberLiteralType.Number: _Num_Start + ".eE_",
    _NumberLiteralType.Real: _Num_Start + "eE_",
    _NumberLiteralType.Exp: _Num_Start + "_",
    _NumberLiteralType.Binary: "01_",
    _NumberLiteralType.Octal: "01234567_",
    _NumberLiteralType.Hex: _Num_Start + "abcdefABCDEF_",
}

_Num_Continue_Next = {
    _NumberLiteralType.Number: {
        '.': _NumberLiteralType.Real,
        'e': _NumberLiteralType.Exp,
        'E': _NumberLiteralType.Exp,
    },
    _NumberLiteralType.Real: {
        'e': _NumberLiteralType.Exp,
        'E': _NumberLiteralType.Exp,
    }
}

_Punctuation_Any = "@$+-*/%~&|^<>=!?{}[]().->,;:"

_Punctuation = (
    "++",  "--",  "@",  "$",  "+",  "-",
    "*",   "/",   "%",  "~",  "&",  "|",
    "^",   "<<",  ">>", "=",  "+=", "-=",
    "*=",  "/=",  "%=", "&=", "|=", "^=",
    "<<=", ">>=", "!",  "&&", "||", "^^",
    "==",  "!=",  "<",  "<=", ">",  ">=",
    "{",   "}",   "[",  "]",  "(",  ")",
    "?",   ".",   "->", ",",  ";",  ":",
)


class LexerError(CompilerError):

    def __init__(self, message: str, file_info: FileInfo):
        super().__init__(message, file_info)


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


def lexer(file: str, filename: str) -> Sequence[Token]:
    tokens: list[Token] = []
    current: str = ""
    current_line: int = 0
    current_col: int = 0
    escaped: bool = False
    number_type: _NumberLiteralType = _NumberLiteralType.Number
    token_type: _InterTokenType = _InterTokenType.Generic

    for line, line_str in enumerate(file.splitlines()):
        fi = FileInfo(filename, current_line, current_col, len(current))
        if token_type in _NewLineErrorTokens:
            raise LexerError("Unexpected Newline", fi)
        if token_type in _NewLineTerminatedTokens:
            if token_type is _InterTokenType.Directive:
                tokens.append(Directive(current, fi))
            elif token_type is _InterTokenType.Word:
                if len(current) > 15:
                    raise LexerError("Identifier Too Long", fi)
                if current in _Keywords:
                    tokens.append(Keyword(current, fi))
                else:
                    tokens.append(Identifier(current, fi))
            elif token_type is _InterTokenType.NumberLiteral:
                tokens.append(NumberLiteral(current, fi))
            elif token_type is _InterTokenType.Punctuation:
                if current not in _Punctuation:
                    raise LexerError("Invalid Punctuation", fi)
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
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    if len(current) > 15:
                        raise LexerError("Identifier Too Long", fi)
                    if current in _Keywords:
                        tokens.append(Keyword(current, fi))
                    else:
                        tokens.append(Identifier(current, fi))
                token_type = _InterTokenType.Generic
            elif token_type is _InterTokenType.NumberLiteral:
                if len(current) == 2 and char in _Num_Second[number_type]:
                    current += char
                    if char in _Num_Second_Next[number_type]:
                        number_type = _Num_Second_Next[number_type][char]
                elif char in _Num_Continue:
                    current += char
                    if char in _Num_Continue_Next[number_type]:
                        number_type = _Num_Continue_Next[number_type][char]
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
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    if (
                        current[1] != '\\' and
                        len(current) == 3 or
                        len(current) > 3
                    ):
                        raise LexerError("Character Literal Too Long", fi)
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
                    fi = FileInfo(
                        filename, current_line, current_col, len(current))
                    if current not in _Punctuation:
                        raise LexerError("Invalid Punctuation", fi)
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
                elif (
                    char == '.' and
                    line_str[col+1] in _Num_Second[_NumberLiteralType.Real]
                ):
                    token_type = _InterTokenType.NumberLiteral
                    if char in _Num_Start_Next[number_type]:
                        number_type = _Num_Start_Next[number_type][char]
                elif char in _Num_Start:
                    token_type = _InterTokenType.NumberLiteral
                    if char in _Num_Start_Next[number_type]:
                        number_type = _Num_Start_Next[number_type][char]
                elif char == "'":
                    token_type = _InterTokenType.CharLiteral
                elif char == '"':
                    token_type = _InterTokenType.StringLiteral
                elif char in _Punctuation_Any:
                    token_type = _InterTokenType.Punctuation

    return tokens
