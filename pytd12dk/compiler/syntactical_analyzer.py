# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import Sequence

from .compiler_types import CompilerError, FileInfo
from . import lexer


type NestableCodeBlock = ForBlock | WhileBlock | DoBlock | IfBlock

type Literal = (
    BuiltInConst |
    NumberLiteral |
    CharLiteral |
    StringLiteral
)

type Expression = (
    Literal |
    Identifier |
    UnaryExpression |
    BinaryExpression |
    TernaryExpression |
    FunctionCall |
    NoOperation
)

type Statement = Expression | LetStatement | LoopStatements | NestableCodeBlock

type DataType = BuiltInDataType | Identifier

type Operator = UnaryOperator | BinaryOperator | TernaryOperator


class SyntaxError(CompilerError):

    _compiler_error_type = "Syntax"


class UnexpectedEndOfTokenStream(SyntaxError): pass


class _ExpectedTokenBase(SyntaxError):

    _token_type = lexer.Token

    def __init__(
        self,
        token: lexer.Token,
        expected: str | None = None,
        found: str | None = None,
    ):
        if expected is None:
            expected = self._token_type.__name__
            found = found or type(token).__name__
        else:
            found = found or token.value
        message = f"Expected '{expected}' but found '{found}'."
        super().__init__(message, token.file_info)


class ExpectedLiteral(_ExpectedTokenBase):

    _token_type = (
        lexer.NumberLiteral,
        lexer.CharLiteral,
        lexer.StringLiteral,
    )

    def __init__(
        self,
        token: lexer.Token,
        expected: str | None = None,
        found: str | None = None,
    ):
        if expected is None:
            expected = "NumberLiteral', 'CharLiteral', or 'StringLiteral"
            found = found or type(token).__name__
        super().__init__(token, expected, found)


class ExpectedDirective(_ExpectedTokenBase):
    _type_name = lexer.Directive
class ExpectedIdentifier(_ExpectedTokenBase):
    _type_name = lexer.Identifier
class ExpectedKeyword(_ExpectedTokenBase):
    _type_name = lexer.Keyword
class ExpectedNumberLiteral(_ExpectedTokenBase):
    _type_name = lexer.NumberLiteral
class ExpectedCharLiteral(_ExpectedTokenBase):
    _type_name = lexer.CharLiteral
class ExpectedStringLiteral(_ExpectedTokenBase):
    _type_name = lexer.StringLiteral
class ExpectedPunctuation(_ExpectedTokenBase):
    _type_name = lexer.Punctuation


class _UnexpectedTokenBase(_ExpectedTokenBase):

    def __init__(
        self,
        token: lexer.Token,
        expected: str | list[str] | None = None,
        found: str | None = None,
    ):
        if isinstance(expected, list):
            if len(expected) > 1:
                s = ""
                for i in expected[:-1]:
                    s += i + "', '"
                s = s[:-1] + "or '" + expected[-1]
                expected = s
            else:
                expected = expected[0]
        super().__init__(token, expected, found)


class UnexpectedToken(_UnexpectedTokenBase):

    def __init__(
        self,
        token: lexer.Token,
        expected: str | list[str],
        found: str | None = None,
    ):
        if isinstance(expected, list):
            if len(expected) > 1:
                s = ""
                for i in expected[:-1]:
                    s += i + "', '"
                s = s[:-1] + "or '" + expected[-1]
                expected = s
        found = found or type(token).__name__
        super().__init__(token, expected, found)


class UnexpectedDirective(_UnexpectedTokenBase):
    _type_name = lexer.Directive
class UnexpectedIdentifier(_UnexpectedTokenBase):
    _type_name = lexer.Identifier
class UnexpectedKeyword(_UnexpectedTokenBase):
    _type_name = lexer.Keyword
class UnexpectedNumberLiteral(_UnexpectedTokenBase):
    _type_name = lexer.NumberLiteral
class UnexpectedCharLiteral(_UnexpectedTokenBase):
    _type_name = lexer.CharLiteral
class UnexpectedStringLiteral(_UnexpectedTokenBase):
    _type_name = lexer.StringLiteral
class UnexpectedPunctuation(_UnexpectedTokenBase):
    _type_name = lexer.Punctuation


class ExpressionError(Exception): pass


class BuiltInConstEnum(Enum):
    ConstTrue = "True"
    ConstFalse = "False"
    ConstNone = "None"


class BuiltInConst:

    _content: BuiltInConstEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: BuiltInConstEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def content(self) -> BuiltInConstEnum: return self._content

    @property
    def value(self) -> int:
        match (self._content):
            case BuiltInConstEnum.ConstTrue: return 1
            case BuiltInConstEnum.ConstFalse: return 0
            case BuiltInConstEnum.ConstNone: return 0

    def __str__(self) -> str: return self._content.value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Built-In Constant: {self._content.value}\n"
        return s


class LoopStatementsEnum(Enum):
    ContinueStatement = "continue"
    BreakStatement = "break"


class LoopStatements:

    _content: LoopStatementsEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: LoopStatementsEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def __str__(self) -> str: return self._content.value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} {self._content.value.lower()}\n"
        return s


class PostfixUnaryOperatorEnum(Enum):
    Increment = "++"
    Decrement = "--"


class PrefixUnaryOperatorEnum(Enum):
    Increment = "++"
    Decrement = "--"
    Negate = "-"
    BitwiseNOT = "~"
    BooleanNOT = "!"
    AddressOf = "@"
    Dereference = "$"


class UnaryOperator:

    _content: PostfixUnaryOperatorEnum | PrefixUnaryOperatorEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: PostfixUnaryOperatorEnum | PrefixUnaryOperatorEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def content(self) -> PostfixUnaryOperatorEnum | PrefixUnaryOperatorEnum:
        return self._content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def __str__(self) -> str: return (
        f"{type(self._content).__name__[:-4]}.{self._content.name}")

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Unary Operator: {self}\n"
        return s


class BinaryOperatorEnum(Enum):
    Addition = "+"
    Subtraction = "-"
    Multiplication = "*"
    Division = "/"
    Modulus = "%"
    BitwiseAND = "&"
    BitwiseOR = "|"
    BitwiseXOR = "^"
    LeftShift = "<<"
    RightShift = ">>"
    MemberOf = "."
    Assignment = "="
    AdditionAssignment = "+="
    SubtractionAssignment = "-="
    MultiplicationAssignment = "*="
    DivisionAssignment = "/="
    ModulusAssignment = "%="
    BitwiseANDAssignment = "&="
    BitwiseORAssignment = "|="
    BitwiseXORAssignment = "^="
    LeftShiftAssignment = "<<="
    RightShiftAssignment = ">>="
    BooleanAND = "&&"
    BooleanOR = "||"
    BooleanXOR = "^^"
    EqualityComparison = "=="
    InequalityComparison = "!="
    LessThan = "<"
    LessOrEqualToThan = "<="
    GreaterThan = ">"
    GreaterOrEqualToThan = ">="


class BinaryOperator:

    _content: BinaryOperatorEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: BinaryOperatorEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def content(self) -> BinaryOperatorEnum: return self._content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def __str__(self) -> str: return (
        f"{type(self._content).__name__[:-4]}.{self._content.name}")

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Binary Operator: {self}\n"
        return s


class TernaryOperatorEnum(Enum):
    TernaryConditional = "?"


class TernaryOperator:

    _content: TernaryOperatorEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: TernaryOperatorEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def content(self) -> TernaryOperatorEnum: return self._content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def __str__(self) -> str: return (
        f"{type(self._content).__name__[:-4]}.{self._content.name}")

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Ternary Operator: {self}\n"
        return s


class BuiltInDataTypeEnum(Enum):
    unsigned = "unsigned"
    int = "int"
    fixed = "fixed"
    float = "float"


class BuiltInDataType:

    _content: BuiltInDataTypeEnum
    _file_info: FileInfo

    def __init__(
        self,
        content: BuiltInDataTypeEnum,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def __str__(self) -> str: return self._content.value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Built-In Data Type: {self._content.value}\n"
        return s


_Operator_Precedence: tuple[
    PostfixUnaryOperatorEnum |
    PrefixUnaryOperatorEnum |
    BinaryOperatorEnum |
    TernaryOperatorEnum,
    ...
] = (
    PrefixUnaryOperatorEnum.AddressOf,
    PrefixUnaryOperatorEnum.Dereference,
    PrefixUnaryOperatorEnum.BitwiseNOT,
    PostfixUnaryOperatorEnum.Decrement,
    PostfixUnaryOperatorEnum.Increment,
    PrefixUnaryOperatorEnum.Decrement,
    PrefixUnaryOperatorEnum.Increment,
    PrefixUnaryOperatorEnum.Negate,
    PrefixUnaryOperatorEnum.BooleanNOT,
    BinaryOperatorEnum.MemberOf,
    BinaryOperatorEnum.RightShift,
    BinaryOperatorEnum.LeftShift,
    BinaryOperatorEnum.BitwiseXOR,
    BinaryOperatorEnum.BitwiseOR,
    BinaryOperatorEnum.BitwiseAND,
    BinaryOperatorEnum.Modulus,
    BinaryOperatorEnum.Division,
    BinaryOperatorEnum.Multiplication,
    BinaryOperatorEnum.Subtraction,
    BinaryOperatorEnum.Addition,
    BinaryOperatorEnum.GreaterOrEqualToThan,
    BinaryOperatorEnum.GreaterThan,
    BinaryOperatorEnum.LessOrEqualToThan,
    BinaryOperatorEnum.LessThan,
    BinaryOperatorEnum.InequalityComparison,
    BinaryOperatorEnum.EqualityComparison,
    BinaryOperatorEnum.BooleanXOR,
    BinaryOperatorEnum.BooleanOR,
    BinaryOperatorEnum.BooleanAND,
    TernaryOperatorEnum.TernaryConditional,
    BinaryOperatorEnum.RightShiftAssignment,
    BinaryOperatorEnum.LeftShiftAssignment,
    BinaryOperatorEnum.BitwiseXORAssignment,
    BinaryOperatorEnum.BitwiseORAssignment,
    BinaryOperatorEnum.BitwiseANDAssignment,
    BinaryOperatorEnum.ModulusAssignment,
    BinaryOperatorEnum.DivisionAssignment,
    BinaryOperatorEnum.MultiplicationAssignment,
    BinaryOperatorEnum.SubtractionAssignment,
    BinaryOperatorEnum.AdditionAssignment,
    BinaryOperatorEnum.Assignment,
)


class NoOperation:

    _file_info: FileInfo

    def __init__(
        self,
        file_info: FileInfo,
    ):
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Nop\n"
        return s


class Identifier:

    _content: str
    _file_info: FileInfo

    def __init__(
        self,
        content: str,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def content(self) -> str: return self._content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Identifier: {self._content}\n"
        return s


class StringLiteral:

    _content: str
    _file_info: FileInfo

    def __init__(
        self,
        content: str,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def content(self) -> str: return self._content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} String Literal: {self._content}\n"
        return s


class CharLiteral:

    _content: str
    _file_info: FileInfo

    def __init__(
        self,
        content: str,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def content(self) -> str: return self._content

    @property
    def value(self) -> int: return ord(self._content)

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Character Literal: {self._content}\n"
        return s


class NumberLiteral:

    _content: str
    _file_info: FileInfo

    def __init__(
        self,
        content: str,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def content(self) -> str: return self._content

    @property
    def value(self) -> int: return int(self._content, base=0)

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Number Literal: {self._content}\n"
        return s


class FunctionArgument:

    _identifier: Identifier | None
    _value: Expression
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier | None,
        value: Expression,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._value = value
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier | None: return self._identifier

    @property
    def value(self) -> Expression: return self._value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function Argument\n"
        if self._identifier: s += f"{pre_cont}├─ Name: {self._identifier}\n"
        s += f"{pre_cont}└─ Value: {self._value}\n"
        return s


class FunctionCall:

    _identifier: Identifier
    _args: list[FunctionArgument]
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        args: list[FunctionArgument],
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._args = args
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def args(self) -> list[FunctionArgument]: return self._args[:]

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function Call: {self._identifier}\n"
        if self._args:
            for arg in self._args[:-1]:
                s += arg.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._args[-1].tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class TernaryExpression:

    _operator: TernaryOperator
    _operand1: Expression
    _operand2: Expression
    _operand3: Expression
    _file_info: FileInfo

    def __init__(
        self,
        operator: TernaryOperator,
        operand1: Expression,
        operand2: Expression,
        operand3: Expression,
        file_info: FileInfo,
    ):
        self._operator = operator
        self._operand1 = operand1
        self._operand2 = operand2
        self._operand3 = operand3
        self._file_info = file_info

    @property
    def operator(self) -> TernaryOperator: return self._operator

    @property
    def operand1(self) -> Expression: return self._operand1

    @property
    def operand2(self) -> Expression: return self._operand2

    @property
    def operand3(self) -> Expression: return self._operand3

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Ternary Expression: {self._operator}\n"
        s += self._operand1.tree_str(pre_cont + "├─", pre_cont + "│ ")
        s += self._operand2.tree_str(pre_cont + "├─", pre_cont + "│ ")
        s += self._operand3.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class BinaryExpression:

    _operator: BinaryOperator
    _operand1: Expression
    _operand2: Expression
    _file_info: FileInfo

    def __init__(
        self,
        operator: BinaryOperator,
        operand1: Expression,
        operand2: Expression,
        file_info: FileInfo,
    ):
        self._operator = operator
        self._operand1 = operand1
        self._operand2 = operand2
        self._file_info = file_info

    @property
    def operator(self) -> BinaryOperator: return self._operator

    @property
    def operand1(self) -> Expression: return self._operand1

    @property
    def operand2(self) -> Expression: return self._operand2

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Binary Expression: {self._operator}\n"
        s += self._operand1.tree_str(pre_cont + "├─", pre_cont + "│ ")
        s += self._operand2.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class UnaryExpression:

    _operator: UnaryOperator
    _operand: Expression
    _file_info: FileInfo

    def __init__(
        self,
        operator: UnaryOperator,
        operand: Expression,
        file_info: FileInfo,
    ):
        self._operator = operator
        self._operand = operand
        self._file_info = file_info

    @property
    def operator(self) -> UnaryOperator: return self._operator

    @property
    def operand(self) -> Expression: return self._operand

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Unary Expression: {self._operator}\n"
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class LetStatement:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _assignment: Literal | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        static: bool,
        assignment: Literal | None,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._static = static
        self._assignment = assignment
        self._file_info = file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def assignment(self) -> Literal | None: return self._assignment

    @property
    def static(self) -> bool: return self._static

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Let Statement: {self._identifier}\n"
        s += pre_cont
        s += '├─ Type: ' if self._assignment else '└─ Type: '
        if self._static: s+= "static "
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        if self._assignment is not None:
            s += f"{pre_cont}└─ Default Value: {self._assignment}\n"
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], token: lexer.Token) -> "LetStatement":
        start_fi: FileInfo = token.file_info
        static = token.value == 'static'
        if static:
            token = tokens.pop(0)
            _assert_token(ExpectedKeyword, token, 'let')
        identifier = tokens.pop(0)
        _assert_token(ExpectedIdentifier, identifier)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, ':')
        pointer, data_type = _data_type_sa(tokens)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token)
        if token.value not in ['=', ';']:
            raise UnexpectedPunctuation(token, ['=', ';'])
        elif token.value == '=':
            token = tokens.pop(0)
            _assert_token_literal(token)
            literal = _literal_map(token) # type: ignore
            token = tokens.pop(0)
            _assert_token(ExpectedPunctuation, token)
            if token.value != ';':
                raise UnexpectedPunctuation(token, ';')
        else: literal = None
        return LetStatement(
            Identifier(identifier.value, identifier.file_info),
            data_type,
            pointer,
            static,
            literal,
            start_fi + token.file_info,
        )


class ElseBlock:

    _code: list[Statement]
    _file_info: FileInfo

    def __init__(
        self,
        code: list[Statement],
        file_info: FileInfo,
    ):
        self._code = code[:]
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def code(self) -> list[Statement]: return self._code[:]

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Else Block\n"
        if self._code:
            s += f"{pre_cont}└─ Code\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._code[-1].tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token]) -> "ElseBlock | None":
        if tokens and tokens[0].value == 'else':
            else_token = tokens.pop(0)
            if tokens[0].value == '{':
                else_tokens = _get_nested_group(tokens, ('{','}'))[1]
                fi = else_token.file_info + else_tokens[-1].file_info
                return ElseBlock(_code_block_sa(else_tokens), fi)
            else:
                statement = _statement_sa(tokens)
                fi = else_token.file_info + statement.file_info
                return ElseBlock([statement], fi)
        else:
            return None


class ForPreDef:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _assignment: Expression | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        assignment: Expression | None,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._assignment = assignment
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def data_type(self) -> DataType: return self._type

    @property
    def pointer(self) -> bool: return self._pointer

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} For Loop Pre-Definition: {self._identifier}\n"
        if self._assignment: s += f"{pre_cont}├─ Type: "
        else: s += f"{pre_cont}└─ Type: "
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        if self._assignment: s += f"{pre_cont}└─ Value: {self._assignment}\n"
        return s


class ForBlock:

    _pre_statement: Expression | ForPreDef
    _condition: Expression
    _code: list[Statement]
    _post_statement: Expression
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        pre_statement: Expression | ForPreDef,
        condition: Expression,
        code: list[Statement],
        post_statement: Expression,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._pre_statement = pre_statement
        self._condition = condition
        self._code = code[:]
        self._post_statement = post_statement
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def pre_statement(self) -> Expression | ForPreDef:
        return self._pre_statement

    @property
    def condition(self) -> Expression: return self._condition

    @property
    def code(self) -> list[Statement]: return self._code[:]

    @property
    def post_statement(self) -> Expression: return self._post_statement

    @property
    def else_block(self) -> ElseBlock | None: return self._else

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} For Loop\n"
        if self._code or self._else is not None:
            cond_pre = f"{pre_cont}├─"
            cond_pre_cont = f"{pre_cont}│ "
        else:
            cond_pre = f"{pre_cont}└─"
            cond_pre_cont = f"{pre_cont}  "
        s += f"{cond_pre} Pre-Statement\n"
        s += self._pre_statement.tree_str(
            cond_pre_cont + "└─", cond_pre_cont + "  ")
        s += f"{cond_pre} Condition\n"
        s += self._condition.tree_str(
            cond_pre_cont + "└─", cond_pre_cont + "  ")
        s += f"{cond_pre} Post-Statement\n"
        s += self._post_statement.tree_str(
            cond_pre_cont + "└─", cond_pre_cont + "  ")
        if self._code:
            if self._else is not None:
                s += f"{pre_cont}├─ Code\n"
                code_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Code\n"
                code_pre = f"{pre_cont}  "
            for code in self._code[:-1]:
                s += code.tree_str(code_pre + "├─", code_pre + "│ ")
            s += self._code[-1].tree_str(code_pre + "└─", code_pre + "  ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], stoken: lexer.Token) -> "ForBlock":
        _, three_expressions, closing_parentheses = _get_nested_group(tokens)
        pre_loop_tokens, semicolon = _get_to_symbol(three_expressions)
        if (
            isinstance(pre_loop_tokens[0], lexer.Identifier) and
            pre_loop_tokens[1].value == ':'
        ):
            id_token = pre_loop_tokens.pop(0)
            identifier = Identifier(id_token.value, id_token.file_info)
            token = pre_loop_tokens.pop(0)
            _assert_token(ExpectedPunctuation, token, ':')
            pointer, data_type = _data_type_sa(pre_loop_tokens)
            if pre_loop_tokens:
                token = pre_loop_tokens.pop(0)
                _assert_token(ExpectedPunctuation, token, '=')
                if not pre_loop_tokens:
                    fi = semicolon.file_info
                    raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
                pre_loop_expr = _expression_sa(pre_loop_tokens)
            else:
                pre_loop_expr = None
            if pre_loop_expr is not None:
                fi = id_token.file_info + pre_loop_expr.file_info
            else:
                fi = id_token.file_info + data_type.file_info
            pre_loop = ForPreDef(
                identifier,
                data_type,
                pointer,
                pre_loop_expr,
                fi,
            )
        else:
            if not pre_loop_tokens:
                fi = semicolon.file_info
                raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
            pre_loop = _expression_sa(pre_loop_tokens)
        loop_condition_tokens, semicolon = _get_to_symbol(three_expressions)
        if not loop_condition_tokens:
            fi = semicolon.file_info
            raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
        condition = _expression_sa(loop_condition_tokens)
        if not three_expressions:
            fi = closing_parentheses.file_info
            raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
        post_loop = _expression_sa(three_expressions)
        if tokens[0].value == '{':
            code = _code_block_sa(_get_nested_group(tokens, ('{','}'))[1])
        else:
            code = [_statement_sa(tokens)]
        else_block = ElseBlock._sa(tokens)
        if else_block is not None:
            fi = stoken.file_info + else_block.file_info
        else:
            fi = stoken.file_info + code[-1].file_info
        return ForBlock(pre_loop, condition, code, post_loop, else_block, fi)


class WhileBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        condition: Expression,
        code: list[Statement],
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._condition = condition
        self._code = code[:]
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def condition(self) -> Expression: return self._condition

    @property
    def code(self) -> list[Statement]: return self._code[:]

    @property
    def else_block(self) -> ElseBlock | None: return self._else

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} While Loop\n"
        if self._code or self._else is not None:
            s += f"{pre_cont}├─ Condition\n"
            cond_pre = f"{pre_cont}│ "
        else:
            s += f"{pre_cont}└─ Condition\n"
            cond_pre = f"{pre_cont}  "
        s += self._condition.tree_str(cond_pre + "└─", cond_pre + "  ")
        if self._code:
            if self._else is not None:
                s += f"{pre_cont}├─ Code\n"
                code_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Code\n"
                code_pre = f"{pre_cont}  "
            for code in self._code[:-1]:
                s += code.tree_str(code_pre + "├─", code_pre + "│ ")
            s += self._code[-1].tree_str(code_pre + "└─", code_pre + "  ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], token: lexer.Token) -> "WhileBlock":
        _, condition_tokens, closing_parentheses = _get_nested_group(tokens)
        if not condition_tokens:
            fi = closing_parentheses.file_info
            raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
        condition = _expression_sa(condition_tokens)
        if tokens[0].value == '{':
            code_tokens = _get_nested_group(tokens, ('{','}'))[1]
            code = _code_block_sa(code_tokens)
        else:
            code = [_statement_sa(tokens)]
        else_block = ElseBlock._sa(tokens)
        if else_block is not None:
            fi = token.file_info + else_block.file_info
        else:
            fi = token.file_info + code[-1].file_info
        return WhileBlock(condition, code, else_block, fi)


class DoBlock:

    _first_code: list[Statement]
    _condition: Expression
    _second_code: list[Statement] | None
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        first_code: list[Statement],
        condition: Expression,
        second_code: list[Statement] | None,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._first_code = first_code[:]
        self._condition = condition
        if second_code:
            self._second_code = second_code[:]
        else:
            self._second_code = None
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def condition(self) -> Expression: return self._condition

    @property
    def first_code(self) -> list[Statement]: return self._first_code[:]

    @property
    def second_code(self) -> list[Statement] | None:
        if self._second_code is None: return None
        else: return self._second_code[:]

    @property
    def else_block(self) -> ElseBlock | None: return self._else

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Do Loop\n"
        if self._first_code:
            s += f"{pre_cont}├─ First Code\n"
            code_pre = f"{pre_cont}│ "
            for code in self._first_code[:-1]:
                s += code.tree_str(code_pre + "├─", code_pre + "│ ")
            s += self._first_code[-1].tree_str(
                code_pre + "└─", code_pre + "  ")
        if self._second_code or self._else is not None:
            s += f"{pre_cont}├─ Condition\n"
            cond_pre = f"{pre_cont}│ "
        else:
            s += f"{pre_cont}└─ Condition\n"
            cond_pre = f"{pre_cont}  "
        s += self._condition.tree_str(cond_pre + "└─", cond_pre + "  ")
        if self._second_code:
            if self._else is not None:
                s += f"{pre_cont}├─ Second Code\n"
                code_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Second Code\n"
                code_pre = f"{pre_cont}  "
            for code in self._second_code[:-1]:
                s += code.tree_str(code_pre + "├─", code_pre + "│ ")
            s += self._second_code[-1].tree_str(
                code_pre + "└─", code_pre + "  ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], stoken: lexer.Token) -> "DoBlock":
        if tokens[0].value == '{':
            code1_tokens = _get_nested_group(tokens, ('{','}'))[1]
            code1 = _code_block_sa(code1_tokens)
        else:
            code1 = [_statement_sa(tokens)]
        token = tokens.pop(0)
        _assert_token(ExpectedKeyword, token, 'while')
        _, condition_tokens, closing_parentheses = _get_nested_group(tokens)
        if not condition_tokens:
            fi = closing_parentheses.file_info
            raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
        last_token = condition_tokens[-1]
        condition = _expression_sa(condition_tokens)
        if tokens[0].value == '{':
            code2_tokens = _get_nested_group(tokens, ('{','}'))[1]
            last_token = code2_tokens[-1]
            code2 = _code_block_sa(code2_tokens)
        elif tokens[0].value != 'else':
            last_token = tokens[0]
            code2 = [_statement_sa(tokens)]
            if isinstance(code2[0], NoOperation):
                code2 = None
        else:
            code2 = None
        else_block = ElseBlock._sa(tokens)
        if else_block is not None:
            fi = stoken.file_info + else_block.file_info
        else:
            fi = stoken.file_info + last_token.file_info
        return DoBlock(code1, condition, code2, else_block, fi)


class IfBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        condition: Expression,
        code: list[Statement],
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._condition = condition
        self._code = code[:]
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def condition(self) -> Expression: return self._condition

    @property
    def code(self) -> list[Statement]: return self._code[:]

    @property
    def else_block(self) -> ElseBlock | None: return self._else

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} If Statement\n"
        if self._code or self._else is not None:
            s += f"{pre_cont}├─ Condition\n"
            cond_pre = f"{pre_cont}│ "
        else:
            s += f"{pre_cont}└─ Condition\n"
            cond_pre = f"{pre_cont}  "
        s += self._condition.tree_str(cond_pre + "└─", cond_pre + "  ")
        if self._code:
            if self._else is not None:
                s += f"{pre_cont}├─ Code\n"
                code_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Code\n"
                code_pre = f"{pre_cont}  "
            for code in self._code[:-1]:
                s += code.tree_str(code_pre + "├─", code_pre + "│ ")
            s += self._code[-1].tree_str(code_pre + "└─", code_pre + "  ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], token: lexer.Token) -> "IfBlock":
        _, condition_tokens, closing_parentheses = _get_nested_group(tokens)
        if not condition_tokens:
            fi = closing_parentheses.file_info
            raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
        condition = _expression_sa(condition_tokens)
        if tokens[0].value == '{':
            code = _code_block_sa(_get_nested_group(tokens, ('{','}'))[1])
        else:
            code = [_statement_sa(tokens)]
        else_block = ElseBlock._sa(tokens)
        if else_block is not None:
            fi = token.file_info + else_block.file_info
        else:
            fi = token.file_info + code[-1].file_info
        return IfBlock(condition, code, else_block, fi)


class FunctionParameter:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _default: Literal | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        default: Literal | None,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._default = default
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function Parameter: {self._identifier}\n"
        s += pre_cont
        s += '├─ Type: ' if self._default else '└─ Type: '
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        if self._default:
            s += f"{pre_cont}└─ Default Value: {self._default}\n"
        return s


class FunctionBlock:

    _identifier: Identifier
    _params: list[FunctionParameter]
    _return_type_pointer: bool
    _return_type: DataType | None
    _code: list[Statement]
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        params: list[FunctionParameter],
        return_type_pointer: bool,
        return_type: DataType | None,
        code: list[Statement],
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._params = params[:]
        self._return_type_pointer = return_type_pointer
        self._return_type = return_type
        self._code = code[:]
        self._file_info = file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def params(self) -> list[FunctionParameter]: return self._params[:]

    @property
    def return_type_pointer(self) -> bool: return self._return_type_pointer

    @property
    def return_type(self) -> DataType | None: return self._return_type

    @property
    def code(self) -> list[Statement]: return self._code[:]

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function: {self._identifier}\n"
        if self._params:
            if self._code or self._return_type is not None:
                s += f"{pre_cont}├─ Parameters\n"
                params_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Parameters\n"
                params_pre = f"{pre_cont}  "
            for param in self._params[:-1]:
                s += param.tree_str(params_pre + "├─", params_pre + "│ ")
            s += self._params[-1].tree_str(params_pre + "└─", params_pre + "  ")
        if self._return_type is not None:
            if self._code:
                s += f"{pre_cont}├─ Return Type: "
            else:
                s += f"{pre_cont}└─ Return Type: "
            if self._return_type_pointer: s+= "@"
            s += f"{self._return_type}\n"
        if self._code:
            s += f"{pre_cont}└─ Code\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._code[-1].tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], stoken: lexer.Token) -> "FunctionBlock":
        identifier = tokens.pop(0)
        _assert_token(ExpectedIdentifier, identifier)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, '(')
        params: list[FunctionParameter] = []
        while token.value != ')':
            token = tokens.pop(0)
            if isinstance(token, lexer.Punctuation):
                _assert_token(ExpectedPunctuation, token, ')')
            elif isinstance(token, lexer.Identifier):
                member_id = Identifier(token.value, token.file_info)
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token, ':')
                pointer, data_type = _data_type_sa(tokens)
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token)
                if token.value not in [',', '=', ')']:
                    raise UnexpectedPunctuation(token, [',', '=', ')'])
                elif token.value == '=':
                    token = tokens.pop(0)
                    _assert_token_literal(token)
                    literal = _literal_map(token) # type: ignore
                    token = tokens.pop(0)
                    _assert_token(ExpectedPunctuation, token)
                    if token.value not in [',', ')']:
                        raise UnexpectedPunctuation(token, [',', ')'])
                else: literal = None
                if literal is not None:
                    fi = member_id.file_info + literal.file_info
                else:
                    fi = member_id.file_info + data_type.file_info
                params.append(FunctionParameter(
                    member_id, data_type, pointer, literal, fi))
            else:
                raise UnexpectedToken(
                    token, ["Keyword", "Identifier", "Punctuation"])
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, '->')
        pointer, return_type = _data_type_sa(tokens)
        code = _code_block_sa(_get_nested_group(tokens, ('{','}'))[1])
        fi = token.file_info + code[-1].file_info
        return FunctionBlock(
            Identifier(identifier.value, identifier.file_info),
            params,
            pointer,
            return_type,
            code,
            fi,
        )


class EnumMember:

    _identifier: Identifier
    _value: NumberLiteral | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        value: NumberLiteral | None,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._value = value
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def value(self) -> NumberLiteral | None: return self._value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Enum Member: {self._identifier}\n"
        if self._value is not None:
            s += f"{pre_cont}└─ Value: {self._value}\n"
        return s


class EnumBlock:

    _identifier: Identifier
    _members: list[EnumMember]
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        members: list[EnumMember],
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._members = members[:]
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    @property
    def members(self) -> list[EnumMember]: return self._members[:]

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Enum: {self._identifier}\n"
        if self._members:
            for member in self._members[:-1]:
                s += member.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._members[-1].tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], stoken: lexer.Token) -> "EnumBlock":
        identifier = tokens.pop(0)
        _assert_token(ExpectedIdentifier, identifier)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, '{')
        members: list[EnumMember] = []
        while token.value != '}':
            token = tokens.pop(0)
            _assert_token(ExpectedIdentifier, token)
            member_id = Identifier(token.value, token.file_info)
            token = tokens.pop(0)
            _assert_token(ExpectedPunctuation, token)
            if token.value not in [',', '=', '}']:
                raise UnexpectedPunctuation(token, [',', '=', '}'])
            elif token.value == '=':
                token = tokens.pop(0)
                _assert_token(ExpectedNumberLiteral, token)
                literal = NumberLiteral(token.value, token.file_info)
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token)
                if token.value not in [',', '}']:
                    raise UnexpectedPunctuation(token, [',', '}'])
            else: literal = None
            if literal is not None:
                fi = member_id.file_info + literal.file_info
            else:
                fi = member_id.file_info
            members.append(EnumMember(member_id, literal, fi))
        fi = stoken.file_info + token.file_info
        return EnumBlock(
            Identifier(identifier.value, identifier.file_info),
            members,
            fi,
        )


class StructureMember:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _default: Literal | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        static: bool,
        default: Literal | None,
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._static = static
        self._default = default
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Struct Member: {self._identifier}\n"
        s += pre_cont
        s += '├─ Type: ' if self._default else '└─ Type: '
        if self._static: s+= "static "
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        if self._default is not None:
            s += f"{pre_cont}└─ Default Value: {self._default}\n"
        return s


class StructBlock:

    _identifier: Identifier
    _members: list[StructureMember]
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        members: list[StructureMember],
        file_info: FileInfo,
    ):
        self._identifier = identifier
        self._members = members[:]
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def identifier(self) -> Identifier: return self._identifier

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Struct: {self._identifier}\n"
        if self._members:
            for member in self._members[:-1]:
                s += member.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._members[-1].tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token], stoken: lexer.Token) -> "StructBlock":
        identifier = tokens.pop(0)
        _assert_token(ExpectedIdentifier, identifier)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, '{')
        members: list[StructureMember] = []
        while token.value != '}':
            token = tokens.pop(0)
            if isinstance(token, lexer.Keyword):
                _assert_token(ExpectedKeyword, token, 'static')
                static_token = token
                token = tokens.pop(0)
                static = True
            else:
                static = False
            if isinstance(token, lexer.Identifier):
                member_id = Identifier(token.value, token.file_info)
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token, ':')
                pointer, data_type = _data_type_sa(tokens)
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token)
                if token.value not in [',', '=', '}']:
                    raise UnexpectedPunctuation(token, [',', '=', '}'])
                elif token.value == '=':
                    token = tokens.pop(0)
                    _assert_token_literal(token)
                    literal = _literal_map(token) # type: ignore
                    token = tokens.pop(0)
                    _assert_token(ExpectedPunctuation, token)
                    if token.value not in [',', '}']:
                        raise UnexpectedPunctuation(token, [',', '}'])
                else: literal = None
                if literal is not None:
                    if static:
                        fi = static_token.file_info + literal.file_info
                    else:
                        fi = member_id.file_info + literal.file_info
                else:
                    if static:
                        fi = static_token.file_info + data_type.file_info
                    else:
                        fi = member_id.file_info + data_type.file_info
                members.append(StructureMember(
                    member_id, data_type, pointer, static, literal, fi))
            else:
                raise UnexpectedToken(token, ["Keyword", "Identifier"])
        fi = stoken.file_info + token.file_info
        return StructBlock(
            Identifier(identifier.value, identifier.file_info),
            members,
            fi,
        )


class Directive:

    _content: str
    _file_info: FileInfo

    def __init__(
        self,
        content: str,
        file_info: FileInfo,
    ):
        self._content = content
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        return f"{pre} Directive: {self._content}\n"


class File:

    _children: list[Directive | StructBlock | FunctionBlock | EnumBlock]
    _file_info: FileInfo

    def __init__(
        self,
        children: list[Directive | StructBlock | FunctionBlock | EnumBlock],
        file_info: FileInfo,
    ):
        self._children = children[:]
        self._file_info = file_info

    @property
    def children(self) -> list[
        Directive |
        StructBlock |
        FunctionBlock |
        EnumBlock
    ]:
        return self._children[:]

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self) -> str:
        s: str = " File\n"
        if self._children:
            for child in self._children[:-1]:
                s += child.tree_str("├─", "│ ")
            s += self._children[-1].tree_str("└─", "  ")
        return s

    @staticmethod
    def _sa(tokens: list[lexer.Token]) -> "File":
        children: list[Directive | StructBlock | FunctionBlock | EnumBlock] = []
        file_fi: FileInfo = tokens[0].file_info + tokens[-1].file_info

        while tokens:
            token = tokens.pop(0)
            _assert_token_mult(token, (lexer.Directive, lexer.Keyword))
            if isinstance(token, lexer.Directive):
                children.append(Directive(token.value, token.file_info))
            elif isinstance(token, lexer.Keyword):
                match token.value:
                    case 'struct':
                        children.append(StructBlock._sa(tokens, token))
                    case 'enum':
                        children.append(EnumBlock._sa(tokens, token))
                    case 'fn':
                        children.append(FunctionBlock._sa(tokens, token))
                    case _:
                        raise ExpectedKeyword(token, "struct', 'enum', or 'fn")
            else:
                raise UnexpectedToken(token, "directive' or 'keyword")

        return File(children, file_fi)


def _assert_token(
    exception: type[_ExpectedTokenBase],
    token: lexer.Token,
    value: str | None = None,
    token_type: type[lexer.Token] | None = None,
):
    if not isinstance(token, token_type or exception._token_type):
        raise exception(token)
    if value is not None and token.value != value:
        raise exception(token, value)

def _assert_token_mult(
    token: lexer.Token,
    token_type: tuple[type[lexer.Token], ...],
):
    if not isinstance(token, token_type):
        raise UnexpectedToken(
            token,
            [i.__name__ for i in token_type], # type: ignore
            type(token).__name__,
        )

def _assert_token_literal(
    token: lexer.Token,
):
    token_types = (
        lexer.Keyword,
        lexer.NumberLiteral,
        lexer.CharLiteral,
        lexer.StringLiteral,
    )
    if not isinstance(token, token_types):
        raise UnexpectedToken(
            token,
            [i.__name__ for i in token_types], # type: ignore
            type(token).__name__,
        )
    if isinstance(token, lexer.Keyword):
        if token.value not in BuiltInConstEnum:
            raise UnexpectedKeyword(
                token, [i.value for i in BuiltInDataTypeEnum])

def _literal_map(literal: (
    lexer.Keyword |
    lexer.NumberLiteral |
    lexer.CharLiteral |
    lexer.StringLiteral
)) -> Literal:
    if isinstance(literal, lexer.Keyword):
        return BuiltInConst(BuiltInConstEnum(literal.value), literal.file_info)
    elif isinstance(literal, lexer.NumberLiteral):
        return NumberLiteral(literal.value, literal.file_info)
    elif isinstance(literal, lexer.CharLiteral):
        return CharLiteral(literal.value, literal.file_info)
    elif isinstance(literal, lexer.StringLiteral):
        return StringLiteral(literal.value, literal.file_info)

def _assert_token_value(
    token: lexer.Token,
):
    token_types = (
        lexer.Identifier,
        lexer.Keyword,
        lexer.NumberLiteral,
        lexer.CharLiteral,
        lexer.StringLiteral,
    )
    if not isinstance(token, token_types):
        raise UnexpectedToken(
            token,
            [i.__name__ for i in token_types], # type: ignore
            type(token).__name__,
        )
    if isinstance(token, lexer.Keyword):
        if token.value not in BuiltInConstEnum:
            raise UnexpectedKeyword(
                token,
                [i.value for i in BuiltInDataTypeEnum]
            )

def _value_map(literal: (
    lexer.Identifier |
    lexer.Keyword |
    lexer.NumberLiteral |
    lexer.CharLiteral |
    lexer.StringLiteral
)) -> Literal | Identifier:
    if isinstance(literal, lexer.Identifier):
        return Identifier(literal.value, literal.file_info)
    elif isinstance(literal, lexer.Keyword):
        return BuiltInConst(BuiltInConstEnum(literal.value), literal.file_info)
    elif isinstance(literal, lexer.NumberLiteral):
        return NumberLiteral(literal.value, literal.file_info)
    elif isinstance(literal, lexer.CharLiteral):
        return CharLiteral(literal.value, literal.file_info)
    elif isinstance(literal, lexer.StringLiteral):
        return StringLiteral(literal.value, literal.file_info)

def _get_nested_group(
    tokens: list[lexer.Token],
    encloses: tuple[str, str] = ('(',')'),
) -> tuple[lexer.Token, list[lexer.Token], lexer.Token]:
    first_token = tokens.pop(0)
    _assert_token(ExpectedPunctuation, first_token, encloses[0])
    nested = 1
    expr_len = -1
    for i in range(len(tokens)):
        if tokens[i].value == encloses[0]: nested += 1
        elif tokens[i].value == encloses[1]: nested -= 1
        if nested == 0:
            expr_len = i
            break
    else:
        raise UnexpectedEndOfTokenStream(
            f"Expected '{encloses[1]}' but found '{tokens[-1].value}'.",
            tokens[-1].file_info,
        )
    expr_tokens = tokens[:expr_len]
    last_token = tokens[expr_len]
    del tokens[:expr_len+1]
    return first_token, expr_tokens, last_token

def _get_to_symbol(
    tokens: list[lexer.Token],
    symbols: str | Sequence[str] = ';',
) -> tuple[list[lexer.Token], lexer.Token]:
    expr_len = -1
    for i in range(len(tokens)):
        if tokens[i].value in symbols:
            expr_len = i
            break
    else:
        raise UnexpectedEndOfTokenStream(
            "Unexpected End of Token Stream.", tokens[-1].file_info)
    expr_tokens = tokens[:expr_len]
    last_token = tokens[expr_len]
    del tokens[:expr_len+1]
    return expr_tokens, last_token

def _data_type_sa(tokens: list[lexer.Token]) -> tuple[bool, DataType]:
    token = tokens.pop(0)
    _assert_token_mult(token, (
        lexer.Keyword,
        lexer.Identifier,
        lexer.Punctuation,
    ))
    if isinstance(token, lexer.Punctuation):
        _assert_token(ExpectedPunctuation, token, '@')
        pointer = True
        token = tokens.pop(0)
        _assert_token_mult(token, (lexer.Keyword, lexer.Identifier))
    else:
        pointer = False
    if isinstance(token, lexer.Keyword):
        if token.value not in BuiltInDataTypeEnum:
            raise UnexpectedKeyword(
                token,
                [i.value for i in BuiltInDataTypeEnum],
            )
        return pointer, BuiltInDataType(
            BuiltInDataTypeEnum(token.value), token.file_info)
    else:
        return pointer, Identifier(token.value, token.file_info)

def _code_block_sa(tokens: list[lexer.Token]) -> list[Statement]:
    code: list[Statement] = []
    while tokens:
        code.append(_statement_sa(tokens))
    return code

def _expression_sa(tokens: list[lexer.Token]) -> Expression:
    if not tokens:
        raise ExpressionError("Expected Expression.")
    elif len(tokens) == 1:
        token = tokens.pop(0)
        _assert_token_value(token)
        return _value_map(token) # type: ignore
    elif tokens[0].value == '(' and tokens[-1].value == ')':
        if not tokens[1:-1]:
            fi = tokens[0].file_info + tokens[-1].file_info
            raise UnexpectedEndOfTokenStream(
                "Expected expression between '(' and ')'.", fi)
        return _expression_sa(tokens[1:-1])

    max_operator: int = -1
    max_operator_precedence: int = -1
    nested = 0
    for i, token in enumerate(tokens):
        if token.value == '(': nested += 1
        elif token.value == ')':
            if nested == 0:
                raise UnexpectedPunctuation(token, "(' before ')", token.value)
            nested -= 1
        elif nested == 0 and isinstance(token, lexer.Punctuation):
            for j, operator in reversed(list(enumerate(_Operator_Precedence))):
                if j <= max_operator_precedence:
                    break
                elif operator.value == token.value:
                    max_operator = i
                    max_operator_precedence = j
                    break

    if max_operator == -1:
        function_identifier = tokens.pop(0)
        _assert_token(ExpectedIdentifier, function_identifier)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token, '(')
        function_args: list[FunctionArgument] = []
        while tokens:
            arg_tokens, last_token = _get_to_symbol(tokens, (',', ')'))
            if arg_tokens:
                if len(arg_tokens) > 1 and arg_tokens[1].value == '=':
                    _assert_token(ExpectedIdentifier, arg_tokens[0])
                    arg_identifier = Identifier(
                        arg_tokens[0].value,
                        arg_tokens[0].file_info,
                    )
                    del arg_tokens[:2]
                else:
                    arg_identifier = None
                if not arg_tokens:
                    fi = last_token.file_info
                    raise UnexpectedEndOfTokenStream("Expected Expression.", fi)
                expression = _expression_sa(arg_tokens)
                if arg_identifier is not None:
                    fi = arg_identifier.file_info + expression.file_info
                else:
                    fi = expression.file_info
                function_args.append(
                    FunctionArgument(arg_identifier, expression, fi))
        fi = function_identifier.file_info + last_token.file_info
        return FunctionCall(
            Identifier(
                function_identifier.value,
                function_identifier.file_info,
            ),
            function_args,
            fi,
        )

    if (
        tokens[max_operator].value in PostfixUnaryOperatorEnum and
        max_operator == len(tokens) - 1
    ):
        operator = UnaryOperator(
            PostfixUnaryOperatorEnum(tokens[max_operator].value),
            tokens[max_operator].file_info,
        )
        if not tokens[:max_operator]:
            fi = tokens[max_operator].file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression before '{tokens[max_operator].value}'.",
                fi,
            )
        expression = _expression_sa(tokens[:max_operator])
        fi = expression.file_info + operator.file_info
        return UnaryExpression(operator, expression, fi)
    elif (
        tokens[max_operator].value in PrefixUnaryOperatorEnum and
        max_operator == 0
    ):
        operator = UnaryOperator(
            PrefixUnaryOperatorEnum(tokens[max_operator].value),
            tokens[max_operator].file_info,
        )
        if not tokens[max_operator + 1:]:
            fi = tokens[max_operator].file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression after '{tokens[max_operator].value}'.",
                fi,
            )
        expression = _expression_sa(tokens[max_operator + 1:])
        fi = operator.file_info + expression.file_info
        return UnaryExpression(operator, expression, fi)
    elif tokens[max_operator].value in BinaryOperatorEnum:
        operator = BinaryOperator(
            BinaryOperatorEnum(tokens[max_operator].value),
            tokens[max_operator].file_info,
        )
        if not tokens[:max_operator]:
            fi = tokens[max_operator].file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression before '{tokens[max_operator].value}'.",
                fi,
            )
        expression1 = _expression_sa(tokens[:max_operator])
        if not tokens[max_operator + 1:]:
            fi = tokens[max_operator].file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression after '{tokens[max_operator].value}'.",
                fi,
            )
        expression2 = _expression_sa(tokens[max_operator + 1:])
        fi = expression1.file_info + expression2.file_info
        return BinaryExpression(operator, expression1, expression2, fi)
    elif tokens[max_operator].value in TernaryOperatorEnum:
        if not tokens[:max_operator]:
            fi = tokens[max_operator].file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression before '{tokens[max_operator].value}'.",
                fi,
            )
        condition = _expression_sa(tokens[:max_operator])
        del tokens[:max_operator]
        operator = TernaryOperator(
            TernaryOperatorEnum.TernaryConditional, tokens[0].file_info)
        first_op, true_tokens, second_op = _get_nested_group(tokens, ('?', ':'))
        if not true_tokens:
            fi = first_op.file_info + second_op.file_info
            raise UnexpectedEndOfTokenStream(
                "Expected expression between "
                f"'{first_op.value}' and '{second_op.value}'.",
                fi,
            )
        true_expr = _expression_sa(true_tokens)
        if not tokens:
            fi = second_op.file_info
            raise UnexpectedEndOfTokenStream(
                f"Expected expression after '{second_op.value}'.",
                fi,
            )
        false_expr = _expression_sa(tokens)
        fi = condition.file_info + false_expr.file_info
        return TernaryExpression(operator, condition, true_expr, false_expr, fi)
    else: raise SyntaxError(
            "Expression Error", tokens[max_operator].file_info)

def _statement_sa(tokens: list[lexer.Token]) -> Statement:
    token = tokens.pop(0)
    if isinstance(token, lexer.Keyword):
        match token.value:
            case 'let' | 'static':
                return LetStatement._sa(tokens, token)
            case 'break' | 'continue' as key:
                fi = token.file_info
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token, ';')
                return LoopStatements(
                    LoopStatementsEnum(key), fi + token.file_info)
            case 'if':
                return IfBlock._sa(tokens, token)
            case 'do':
                return DoBlock._sa(tokens, token)
            case 'while':
                return WhileBlock._sa(tokens, token)
            case 'for':
                return ForBlock._sa(tokens, token)
            case key if key not in BuiltInConstEnum:
                raise UnexpectedKeyword(token, [
                    'static',
                    'let',
                    'break',
                    'continue',
                    'if',
                    'do',
                    'while',
                    'for',
                ] + [i.value for i in BuiltInConstEnum])
    elif token.value == ';':
        return NoOperation(token.file_info)
    expr_tokens: list[lexer.Token] = [token] + _get_to_symbol(tokens)[0]
    return _expression_sa(expr_tokens)

def syntactical_analyzer(tokens: Sequence[lexer.Token]) -> File:
    return File._sa(list(tokens))
