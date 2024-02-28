# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import Sequence

from .compiler_types import CompilerError, FileInfo
from . import lexer


class _ExpectedTokenBase(CompilerError):

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
                s = s[:-1] + "or '" + i
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
                s = s[:-1] + "or '" + i
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


type NestableCodeBlock = ForBlock | WhileBlock | DoBlock | IfBlock

type Literal = (
    BuildInConst |
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
    FunctionCall
)

type Statement = Expression | LetStatement | LoopStatements | NestableCodeBlock

type DataType = DefaultDataType | Identifier


class BuildInConst(Enum):
    ConstTrue = "True"
    ConstFalse = "False"
    ConstNone = "None"


class LoopStatements(Enum):
    ContinueStatement = "continue"
    BreakStatement = "break"


class UnaryOperator(Enum):
    PostfixIncrement = "++"
    PostfixDecrement = "--"
    PrefixIncrement = "++"
    PrefixDecrement = "--"
    Negate = "-"
    BitwiseNOT = "~"
    BooleanNOT = "!"
    Addressof = "@"
    Dereference = "$"


class BinaryOperator(Enum):
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


class DefaultDataType(Enum):
    unsigned = "unsigned"
    int = "int"
    fixed = "fixed"
    float = "float"


_Operator_Precedence = [
    BinaryOperator.Assignment,
    BinaryOperator.AdditionAssignment,
    BinaryOperator.SubtractionAssignment,
    BinaryOperator.MultiplicationAssignment,
    BinaryOperator.DivisionAssignment,
    BinaryOperator.ModulusAssignment,
    BinaryOperator.BitwiseANDAssignment,
    BinaryOperator.BitwiseORAssignment,
    BinaryOperator.BitwiseXORAssignment,
    BinaryOperator.LeftShiftAssignment,
    BinaryOperator.RightShiftAssignment,
    BinaryOperator.BooleanAND,
    BinaryOperator.BooleanOR,
    BinaryOperator.BooleanXOR,
    BinaryOperator.EqualityComparison,
    BinaryOperator.InequalityComparison,
    BinaryOperator.LessThan,
    BinaryOperator.LessOrEqualToThan,
    BinaryOperator.GreaterThan,
    BinaryOperator.GreaterOrEqualToThan,
    BinaryOperator.Addition,
    BinaryOperator.Subtraction,
    BinaryOperator.Multiplication,
    BinaryOperator.Division,
    BinaryOperator.Modulus,
    BinaryOperator.BitwiseAND,
    BinaryOperator.BitwiseOR,
    BinaryOperator.BitwiseXOR,
    BinaryOperator.LeftShift,
    BinaryOperator.RightShift,
    UnaryOperator.BooleanNOT,
    UnaryOperator.Negate,
    UnaryOperator.PrefixIncrement,
    UnaryOperator.PrefixDecrement,
    UnaryOperator.PostfixIncrement,
    UnaryOperator.PostfixDecrement,
    UnaryOperator.BitwiseNOT,
    UnaryOperator.Dereference,
    UnaryOperator.Addressof,
]


class Identifier:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content


class StringLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content


class CharLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content


class NumberLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content


class ArraySubscription:

    _identifier: Identifier
    _index: Expression

    def __init__(
        self,
        identifier: Identifier,
        index: Expression,
    ):
        self._identifier = identifier
        self._index = index


class FunctionArgument:

    _identifier: Identifier | None
    _value: Expression

    def __init__(
        self,
        identifier: Identifier,
        value: Expression,
    ):
        self._identifier = identifier
        self._value = value


class FunctionCall:

    _identifier: Identifier
    _params: list[FunctionArgument]

    def __init__(
        self,
        identifier: Identifier,
        params: list[FunctionArgument],
    ):
        self._identifier = identifier
        self._params = params


class TernaryExpression:

    _operand1: Expression
    _operand2: Expression
    _operand3: Expression

    def __init__(
        self,
        operand1: Expression,
        operand2: Expression,
        operand3: Expression,
    ):
        self._operand1 = operand1
        self._operand2 = operand2
        self._operand3 = operand3


class BinaryExpression:

    _operator: BinaryOperator
    _operand1: Expression
    _operand2: Expression

    def __init__(
        self,
        operator: BinaryOperator,
        operand1: Expression,
        operand2: Expression,
    ):
        self._operator = operator
        self._operand1 = operand1
        self._operand2 = operand2


class UnaryExpression:

    _operator: UnaryOperator
    _operand: Expression

    def __init__(
        self,
        operator: UnaryOperator,
        operand: Expression,
    ):
        self._operator = operator
        self._operand = operand


class LetStatement:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _assignment: Expression | None

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        static: bool,
        assignment: Literal | None,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._static = static
        self._assignment = assignment


class ElseBlock:

    _code: list[Statement]

    def __init__(
        self,
        code: list[Statement],
    ):
        self._code = code[:]


class ForPreDef:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _assignment: Expression

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        default: Literal | None,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._default = default


class ForBlock:

    _pre_statement: Expression | ForPreDef
    _condition: Expression
    _code: list[Statement]
    _post_statement: Expression
    _else: ElseBlock | None

    def __init__(
        self,
        pre_statement: Expression | ForPreDef,
        condition: Expression,
        code: list[Statement],
        post_statement: Expression,
        else_block: ElseBlock | None,
    ):
        self._pre_statement = pre_statement
        self._condition = condition
        self._code = code[:]
        self._post_statement = post_statement
        self._else = else_block


class WhileBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None

    def __init__(
        self,
        condition: Expression,
        code: list[Statement],
        else_block: ElseBlock | None,
    ):
        self._condition = condition
        self._code = code[:]
        self._else = else_block


class DoBlock:

    _first_code: list[Statement]
    _condition: Expression
    _second_code: list[Statement]
    _else: ElseBlock | None

    def __init__(
        self,
        first_code: list[Statement],
        condition: Expression,
        second_code: list[Statement],
        else_block: ElseBlock | None,
    ):
        self._first_code = first_code[:]
        self._condition = condition
        self._second_code = second_code[:]
        self._else = else_block


class IfBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None

    def __init__(
        self,
        condition: Expression,
        code: list[Statement],
        else_block: ElseBlock | None,
    ):
        self._condition = condition
        self._code = code[:]
        self._else = else_block


class FunctionParameter:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _default: Literal | None

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        default: Literal | None,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._default = default


class FunctionBlock:

    _identifier: Identifier
    _args: list[FunctionParameter]
    _return_type: DataType
    _code: list[Statement]

    def __init__(
        self,
        identifier: Identifier,
        args: list[FunctionParameter],
        return_type: DataType,
        code: list[Statement],
    ):
        self._identifier = identifier
        self._args = args[:]
        self._return_type = return_type
        self._code = code[:]


class EnumMember:

    _identifier: Identifier
    _value: NumberLiteral | None

    def __init__(
        self,
        identifier: Identifier,
        value: NumberLiteral | None,
    ):
        self._identifier = identifier
        self._value = value


class EnumBlock:

    _identifier: Identifier
    _members: list[EnumMember]

    def __init__(
        self,
        identifier: Identifier,
        members: list[EnumMember],
    ):
        self._identifier = identifier
        self._members = members[:]


class StructureMember:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _default: Literal | None

    def __init__(
        self,
        identifier: Identifier,
        type: DataType,
        pointer: bool,
        static: bool,
        default: Literal | None,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._static = static
        self._default = default


class StructBlock:

    _identifier: Identifier
    _members: list[StructureMember]

    def __init__(
        self,
        identifier: Identifier,
        members: list[StructureMember],
    ):
        self._identifier = identifier
        self._members = members[:]


class Directive:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content


class File:

    _children: list[Directive | StructBlock | FunctionBlock | EnumBlock]

    def __init__(
        self,
        children: list[Directive | StructBlock | FunctionBlock | EnumBlock],
    ):
        self._children = children[:]


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
        raise ExpectedLiteral(
            token,
            [i.__name__ for i in token_types], # type: ignore
            type(token).__name__,
        )
    if isinstance(token, lexer.Keyword):
        if token.value not in BuildInConst:
            raise UnexpectedKeyword(token, [i.value for i in DefaultDataType])

def _literal_map(literal: (
    lexer.Keyword |
    lexer.NumberLiteral |
    lexer.CharLiteral |
    lexer.StringLiteral
)) -> Literal:
    if isinstance(literal, lexer.Keyword):
        return BuildInConst(literal.value)
    elif isinstance(literal, lexer.NumberLiteral):
        return NumberLiteral(literal.value)
    elif isinstance(literal, lexer.CharLiteral):
        return CharLiteral(literal.value)
    elif isinstance(literal, lexer.StringLiteral):
        return StringLiteral(literal.value)

def struct_syntactical_analyzer(tokens: list[lexer.Token]) -> StructBlock:
    identifier = tokens.pop(0)
    _assert_token(ExpectedIdentifier, identifier)
    temp = tokens.pop(0)
    _assert_token(ExpectedPunctuation, temp, '{')
    members: list[StructureMember] = []
    while temp.value != '}':
        temp = tokens.pop(0)
        if isinstance(temp, lexer.Keyword):
            _assert_token(ExpectedKeyword, temp, 'static')
            temp = tokens.pop(0)
            static = True
        else:
            static = False
        if isinstance(temp, lexer.Identifier):
            member_id = Identifier(temp.value)
            temp = tokens.pop(0)
            _assert_token(ExpectedPunctuation, temp, ':')
            temp = tokens.pop(0)
            _assert_token_mult(temp, (
                lexer.Keyword,
                lexer.Identifier,
                lexer.Punctuation,
            ))
            if isinstance(temp, lexer.Punctuation):
                _assert_token(ExpectedPunctuation, temp, '*')
                pointer = True
                temp = tokens.pop(0)
                _assert_token_mult(temp, (lexer.Keyword, lexer.Identifier))
            else:
                pointer = False
            if isinstance(temp, lexer.Keyword):
                if temp.value not in DefaultDataType:
                    raise UnexpectedKeyword(
                        temp,
                        [i.value for i in DefaultDataType],
                    )
                data_type = DefaultDataType(temp.value)
            else:
                data_type = Identifier(temp.value)
            temp = tokens.pop(0)
            _assert_token(ExpectedPunctuation, temp)
            if temp.value not in [',', '=']:
                raise UnexpectedPunctuation(temp, [',', '='])
            elif temp.value == '=':
                temp = tokens.pop(0)
                _assert_token_literal(temp)
                literal = _literal_map(temp) # type: ignore
                temp = tokens.pop(0)
                _assert_token(ExpectedPunctuation, temp, ',')
            else: literal = None
            members.append(
                StructureMember(member_id, data_type, pointer, static, literal))
        else:
            raise UnexpectedToken(temp, ["Keyword", "Identifier"])
    return StructBlock(Identifier(identifier.value), members)

def enumeration_syntactical_analyzer(tokens: list[lexer.Token]) -> EnumBlock:
    identifier = tokens.pop(0)
    _assert_token(ExpectedIdentifier, identifier)
    temp = tokens.pop(0)
    _assert_token(ExpectedPunctuation, temp, '{')
    members: list[EnumMember] = []
    while temp.value != '}':
        temp = tokens.pop(0)
        _assert_token(ExpectedIdentifier, temp)
        member_id = Identifier(temp.value)
        temp = tokens.pop(0)
        _assert_token(ExpectedPunctuation, temp)
        if temp.value not in [',', '=']:
            raise UnexpectedPunctuation(temp, [',', '='])
        elif temp.value == '=':
            temp = tokens.pop(0)
            _assert_token(ExpectedNumberLiteral, temp)
            temp = tokens.pop(0)
            _assert_token(ExpectedPunctuation, temp, ',')
        else: literal = None
        members.append(EnumMember(member_id, literal))
    return EnumBlock(Identifier(identifier.value), members)

def function_syntactical_analyzer(tokens: list[lexer.Token]) -> FunctionBlock:
    pass

def file_syntactical_analyzer(tokens: list[lexer.Token]) -> File:
    children: list[Directive | StructBlock | FunctionBlock | EnumBlock] = []

    while tokens:
        token = tokens.pop(0)
        _assert_token_mult(token, (lexer.Directive, lexer.Keyword))
        if isinstance(token, lexer.Directive):
            children.append(Directive(token.value))
        elif isinstance(token, lexer.Keyword):
            match token.value:
                case 'struct':
                    children.append(
                        struct_syntactical_analyzer(tokens))
                case 'enum':
                    children.append(
                        enumeration_syntactical_analyzer(tokens))
                case 'fn':
                    children.append(
                        function_syntactical_analyzer(tokens))
                case _:
                    raise ExpectedKeyword(token, "struct', 'enum', or 'fn")

    return File(children)


def syntactical_analyzer(tokens: Sequence[lexer.Token]) -> File:
    return file_syntactical_analyzer(list(tokens))

