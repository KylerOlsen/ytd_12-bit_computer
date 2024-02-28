# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import ClassVar, Sequence

from .compiler_types import CompilerError, FileInfo
from . import lexer


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


class StringLiteral:

    _content: str


class CharLiteral:

    _content: str


class NumberLiteral:

    _content: str


class ArraySubscription:

    _identifier: Identifier
    _index: Expression


class FunctionParameter:

    _identifier: Identifier | None
    _value: Expression


class FunctionCall:

    _identifier: Identifier
    _params: list[FunctionParameter]


class TernaryExpression:

    _operand1: Expression
    _operand2: Expression
    _operand3: Expression


class BinaryExpression:

    _operator: BinaryOperator
    _operand1: Expression
    _operand2: Expression


class UnaryExpression:

    _operator: UnaryOperator
    _operand: Expression


class LetStatement:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _assignment: Expression | None


class ElseBlock:

    _code: list[Statement]


class ForPreDef:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _assignment: Expression


class ForBlock:

    _pre_statement: Expression | ForPreDef
    _condition: Expression
    _code: list[Statement]
    _post_statement: Expression
    _else: ElseBlock | None


class WhileBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None


class DoBlock:

    _first_code: list[Statement]
    _condition: Expression
    _second_code: list[Statement]
    _else: ElseBlock | None


class IfBlock:

    _condition: Expression
    _code: list[Statement]
    _else: ElseBlock | None


class FunctionArgument:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _default: Literal | None


class FunctionBlock:

    _identifier: str
    _public: bool
    _args: list[FunctionArgument]
    _return_type: DataType
    _code: list[Statement]


class EnumMember:

    _identifier: Identifier
    _value: NumberLiteral | None


class EnumBlock:

    _identifier: str
    _public: bool
    _members: list[EnumMember]


class StructureMember:

    _identifier: Identifier
    _type: DataType
    _pointer: bool
    _static: bool
    _default: Literal | None


class StructBlock:

    _identifier: Identifier
    _public: bool
    _members: list[StructureMember]


class Directive:

    _content: str


class File:

    _children: list[Directive | StructBlock | FunctionBlock | EnumBlock]
