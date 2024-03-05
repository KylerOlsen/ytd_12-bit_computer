# Kyler Olsen
# Feb 2024

from enum import Enum
from typing import Sequence

from .compiler_types import CompilerError# , FileInfo
from . import lexer


    # _file_info: FileInfo

    #     file_info: FileInfo,

    #     self._file_info = file_info

class UnexpectedEndOfTokenStream(CompilerError): pass


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
    FunctionCall
)

type Statement = Expression | LetStatement | LoopStatements | NestableCodeBlock

type DataType = BuiltInDataType | Identifier

type UnaryOperator = PostfixUnaryOperator | PrefixUnaryOperator


class BuiltInConst(Enum):
    ConstTrue = "True"
    ConstFalse = "False"
    ConstNone = "None"

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Built-In Constant: {self.value}\n"
        return s


class LoopStatements(Enum):
    ContinueStatement = "continue"
    BreakStatement = "break"

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} {self.value.upper()}\n"
        return s


class PostfixUnaryOperator(Enum):
    Increment = "++"
    Decrement = "--"


class PrefixUnaryOperator(Enum):
    Increment = "++"
    Decrement = "--"
    Negate = "-"
    BitwiseNOT = "~"
    BooleanNOT = "!"
    AddressOf = "@"
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


class TernaryOperator(Enum):
    TernaryConditional = "?"


class BuiltInDataType(Enum):
    unsigned = "unsigned"
    int = "int"
    fixed = "fixed"
    float = "float"


_Operator_Precedence: tuple[
    UnaryOperator | BinaryOperator | TernaryOperator, ...
] = (
    PrefixUnaryOperator.AddressOf,
    PrefixUnaryOperator.Dereference,
    PrefixUnaryOperator.BitwiseNOT,
    PostfixUnaryOperator.Decrement,
    PostfixUnaryOperator.Increment,
    PrefixUnaryOperator.Decrement,
    PrefixUnaryOperator.Increment,
    PrefixUnaryOperator.Negate,
    PrefixUnaryOperator.BooleanNOT,
    BinaryOperator.RightShift,
    BinaryOperator.LeftShift,
    BinaryOperator.BitwiseXOR,
    BinaryOperator.BitwiseOR,
    BinaryOperator.BitwiseAND,
    BinaryOperator.Modulus,
    BinaryOperator.Division,
    BinaryOperator.Multiplication,
    BinaryOperator.Subtraction,
    BinaryOperator.Addition,
    BinaryOperator.GreaterOrEqualToThan,
    BinaryOperator.GreaterThan,
    BinaryOperator.LessOrEqualToThan,
    BinaryOperator.LessThan,
    BinaryOperator.InequalityComparison,
    BinaryOperator.EqualityComparison,
    BinaryOperator.BooleanXOR,
    BinaryOperator.BooleanOR,
    BinaryOperator.BooleanAND,
    TernaryOperator.TernaryConditional,
    BinaryOperator.RightShiftAssignment,
    BinaryOperator.LeftShiftAssignment,
    BinaryOperator.BitwiseXORAssignment,
    BinaryOperator.BitwiseORAssignment,
    BinaryOperator.BitwiseANDAssignment,
    BinaryOperator.ModulusAssignment,
    BinaryOperator.DivisionAssignment,
    BinaryOperator.MultiplicationAssignment,
    BinaryOperator.SubtractionAssignment,
    BinaryOperator.AdditionAssignment,
    BinaryOperator.Assignment,
)


class Identifier:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Identifier: {self._content}\n"
        return s


class StringLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} String Literal: {self._content}\n"
        return s


class CharLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Character Literal: {self._content}\n"
        return s


class NumberLiteral:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content

    def __str__(self) -> str: return self._content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Number Literal: {self._content}\n"
        return s


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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Array Subscription: {self._identifier}\n"
        s += f"{pre_cont}└─ Index: {self._index}\n"
        return s


class FunctionArgument:

    _identifier: Identifier | None
    _value: Expression

    def __init__(
        self,
        identifier: Identifier | None,
        value: Expression,
    ):
        self._identifier = identifier
        self._value = value

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function Argument\n"
        if self._identifier: s += f"{pre_cont}├─ Name: {self._identifier}\n"
        s += f"{pre_cont}└─ Value: {self._value}\n"
        return s


class FunctionCall:

    _identifier: Identifier
    _args: list[FunctionArgument]

    def __init__(
        self,
        identifier: Identifier,
        args: list[FunctionArgument],
    ):
        self._identifier = identifier
        self._args = args

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

    def __init__(
        self,
        operator: TernaryOperator,
        operand1: Expression,
        operand2: Expression,
        operand3: Expression,
    ):
        self._operator = operator
        self._operand1 = operand1
        self._operand2 = operand2
        self._operand3 = operand3

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

    def __init__(
        self,
        operator: BinaryOperator,
        operand1: Expression,
        operand2: Expression,
    ):
        self._operator = operator
        self._operand1 = operand1
        self._operand2 = operand2

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Binary Expression: {self._operator}\n"
        s += self._operand1.tree_str(pre_cont + "├─", pre_cont + "│ ")
        s += self._operand2.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Unary Expression: {self._operator}\n"
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


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


class ElseBlock:

    _code: list[Statement]

    def __init__(
        self,
        code: list[Statement],
    ):
        self._code = code[:]

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Else Block\n"
        if self._code:
            s += f"{pre_cont}└─ Code\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._code[-1].tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s


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
        assignment: Expression,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer
        self._assignment = assignment

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} For Loop Pre-Definition: {self._identifier}\n"
        s += f"{pre_cont}├─ Type: "
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        s += f"{pre_cont}└─ Value: {self._assignment}\n"
        return s


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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} If Statement\n"
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


class DoBlock:

    _first_code: list[Statement]
    _condition: Expression
    _second_code: list[Statement] | None
    _else: ElseBlock | None

    def __init__(
        self,
        first_code: list[Statement],
        condition: Expression,
        second_code: list[Statement] | None,
        else_block: ElseBlock | None,
    ):
        self._first_code = first_code[:]
        self._condition = condition
        if second_code:
            self._second_code = second_code[:]
        else:
            self._second_code = None
        self._else = else_block

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Do Loop\n"
        if self._first_code:
            if self._second_code or self._else is not None:
                s += f"{pre_cont}├─ First Code\n"
                code_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ First Code\n"
                code_pre = f"{pre_cont}  "
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

    def __init__(
        self,
        identifier: Identifier,
        params: list[FunctionParameter],
        return_type_pointer: bool,
        return_type: DataType | None,
        code: list[Statement],
    ):
        self._identifier = identifier
        self._params = params[:]
        self._return_type_pointer = return_type_pointer
        self._return_type = return_type
        self._code = code[:]

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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Enum Member: {self._identifier}\n"
        if self._value is not None:
            s += f"{pre_cont}└─ Value: {self._value}\n"
        return s


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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Enum: {self._identifier}\n"
        if self._members:
            for member in self._members[:-1]:
                s += member.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._members[-1].tree_str(pre_cont + "└─", pre_cont + "│ ")
        return s


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

    def __init__(
        self,
        identifier: Identifier,
        members: list[StructureMember],
    ):
        self._identifier = identifier
        self._members = members[:]

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Struct: {self._identifier}\n"
        if self._members:
            for member in self._members[:-1]:
                s += member.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._members[-1].tree_str(pre_cont + "└─", pre_cont + "│ ")
        return s


class Directive:

    _content: str

    def __init__(
        self,
        content: str,
    ):
        self._content = content

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        return f"{pre} Directive: {self._content}\n"


class File:

    _children: list[Directive | StructBlock | FunctionBlock | EnumBlock]

    def __init__(
        self,
        children: list[Directive | StructBlock | FunctionBlock | EnumBlock],
    ):
        self._children = children[:]

    def tree_str(self) -> str:
        s: str = "File\n"
        if self._children:
            for child in self._children[:-1]:
                s += child.tree_str("├─", "│ ")
            s += self._children[-1].tree_str("└─", "  ")
        return s


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
        if token.value not in BuiltInConst:
            raise UnexpectedKeyword(token, [i.value for i in BuiltInDataType])

def _literal_map(literal: (
    lexer.Keyword |
    lexer.NumberLiteral |
    lexer.CharLiteral |
    lexer.StringLiteral
)) -> Literal:
    if isinstance(literal, lexer.Keyword):
        return BuiltInConst(literal.value)
    elif isinstance(literal, lexer.NumberLiteral):
        return NumberLiteral(literal.value)
    elif isinstance(literal, lexer.CharLiteral):
        return CharLiteral(literal.value)
    elif isinstance(literal, lexer.StringLiteral):
        return StringLiteral(literal.value)

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
        raise ExpectedLiteral(
            token,
            [i.__name__ for i in token_types], # type: ignore
            type(token).__name__,
        )
    if isinstance(token, lexer.Keyword):
        if token.value not in BuiltInConst:
            raise UnexpectedKeyword(token, [i.value for i in BuiltInDataType])

def _value_map(literal: (
    lexer.Identifier |
    lexer.Keyword |
    lexer.NumberLiteral |
    lexer.CharLiteral |
    lexer.StringLiteral
)) -> Literal | Identifier:
    if isinstance(literal, lexer.Identifier):
        return Identifier(literal.value)
    elif isinstance(literal, lexer.Keyword):
        return BuiltInConst(literal.value)
    elif isinstance(literal, lexer.NumberLiteral):
        return NumberLiteral(literal.value)
    elif isinstance(literal, lexer.CharLiteral):
        return CharLiteral(literal.value)
    elif isinstance(literal, lexer.StringLiteral):
        return StringLiteral(literal.value)

def _get_nested_group(
    tokens: list[lexer.Token],
    encloses: tuple[str, str] = ('(',')'),
) -> list[lexer.Token]:
    token = tokens.pop(0)
    _assert_token(ExpectedPunctuation, token, encloses[0])
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
            "Unexpected End of Token Stream.", tokens[-1].file_info)
    expr_tokens = tokens[:expr_len]
    del tokens[:expr_len+1]
    return expr_tokens

def _get_to_symbol(
    tokens: list[lexer.Token],
    symbols: str | Sequence[str] = ';',
) -> list[lexer.Token]:
    expr_len = -1
    for i in range(len(tokens)):
        if tokens[i].value in symbols:
            expr_len = i
            break
    else:
        raise UnexpectedEndOfTokenStream(
            "Unexpected End of Token Stream.", tokens[-1].file_info)
    expr_tokens = tokens[:expr_len]
    del tokens[:expr_len+1]
    return expr_tokens

def _struct_sa(tokens: list[lexer.Token]) -> StructBlock:
    identifier = tokens.pop(0)
    _assert_token(ExpectedIdentifier, identifier)
    token = tokens.pop(0)
    _assert_token(ExpectedPunctuation, token, '{')
    members: list[StructureMember] = []
    while token.value != '}':
        token = tokens.pop(0)
        if isinstance(token, lexer.Keyword):
            _assert_token(ExpectedKeyword, token, 'static')
            token = tokens.pop(0)
            static = True
        else:
            static = False
        if isinstance(token, lexer.Identifier):
            member_id = Identifier(token.value)
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
            members.append(
                StructureMember(member_id, data_type, pointer, static, literal))
        else:
            raise UnexpectedToken(token, ["Keyword", "Identifier"])
    return StructBlock(Identifier(identifier.value), members)

def _enumeration_sa(tokens: list[lexer.Token]) -> EnumBlock:
    identifier = tokens.pop(0)
    _assert_token(ExpectedIdentifier, identifier)
    token = tokens.pop(0)
    _assert_token(ExpectedPunctuation, token, '{')
    members: list[EnumMember] = []
    while token.value != '}':
        token = tokens.pop(0)
        _assert_token(ExpectedIdentifier, token)
        member_id = Identifier(token.value)
        token = tokens.pop(0)
        _assert_token(ExpectedPunctuation, token)
        if token.value not in [',', '=', '}']:
            raise UnexpectedPunctuation(token, [',', '=', '}'])
        elif token.value == '=':
            token = tokens.pop(0)
            _assert_token(ExpectedNumberLiteral, token)
            token = tokens.pop(0)
            _assert_token(ExpectedPunctuation, token)
            if token.value not in [',', '}']:
                raise UnexpectedPunctuation(token, [',', '}'])
        else: literal = None
        members.append(EnumMember(member_id, literal))
    return EnumBlock(Identifier(identifier.value), members)

def _function_sa(tokens: list[lexer.Token]) -> FunctionBlock:
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
            member_id = Identifier(token.value)
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
            params.append(
                FunctionParameter(member_id, data_type, pointer, literal))
        else:
            raise UnexpectedToken(
                token, ["Keyword", "Identifier", "Punctuation"])
    token = tokens.pop(0)
    _assert_token(ExpectedPunctuation, token, '->')
    pointer, return_type = _data_type_sa(tokens)
    code = _code_block_sa(_get_nested_group(tokens, ('{','}')))
    return FunctionBlock(
        Identifier(identifier.value),
        params,
        pointer,
        return_type,
        code,
    )

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
        if token.value not in BuiltInDataType:
            raise UnexpectedKeyword(
                token,
                [i.value for i in BuiltInDataType],
            )
        return pointer, BuiltInDataType(token.value)
    else:
        return pointer, Identifier(token.value)

def _code_block_sa(tokens: list[lexer.Token]) -> list[Statement]:
    code: list[Statement] = []
    while tokens:
        code.append(_statement_sa(tokens))
    return code

def _expression_sa(tokens: list[lexer.Token]) -> Expression:
    print([(type(i).__name__, i.value) for i in tokens])
    if not tokens:
        raise UnexpectedEndOfTokenStream(
            "Unexpected Expression.", None) # type: ignore
    if tokens[0].value == '(' and tokens[-1].value == ')':
        return _expression_sa(tokens[1:-1])
    elif len(tokens) == 1:
        token = tokens.pop(0)
        _assert_token_value(token)
        return _value_map(token) # type: ignore

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
            arg_tokens = _get_to_symbol(tokens, (',', ')'))
            if arg_tokens:
                if len(arg_tokens) > 1 and arg_tokens[1].value == '=':
                    _assert_token(ExpectedIdentifier, arg_tokens[0])
                    arg_identifier = Identifier(arg_tokens[0].value)
                    del arg_tokens[:2]
                else:
                    arg_identifier = None
                function_args.append(FunctionArgument(
                    arg_identifier, _expression_sa(arg_tokens)))
        return FunctionCall(
            Identifier(function_identifier.value), function_args)

    if (
        tokens[max_operator].value in PostfixUnaryOperator and
        max_operator == len(tokens) - 1
    ):
        return UnaryExpression(
            PostfixUnaryOperator(tokens[max_operator].value),
            _expression_sa(tokens[:max_operator]),
        )
    elif (
        tokens[max_operator].value in PrefixUnaryOperator and
        max_operator == 0
    ):
        return UnaryExpression(
            PrefixUnaryOperator(tokens[max_operator].value),
            _expression_sa(tokens[max_operator+1:]),
        )
    elif tokens[max_operator].value in BinaryOperator:
            return BinaryExpression(
                BinaryOperator(tokens[max_operator].value),
                _expression_sa(tokens[:max_operator]),
                _expression_sa(tokens[max_operator+1:]),
            )
    elif tokens[max_operator].value in TernaryOperator:
        condition = _expression_sa(tokens[:max_operator])
        del tokens[:max_operator]
        true_expr = _expression_sa(_get_nested_group(tokens, ('?', ':')))
        false_expr = _expression_sa(tokens)
        return TernaryExpression(
            TernaryOperator.TernaryConditional,
            condition,
            true_expr,
            false_expr,
        )
    else: raise CompilerError(
            "Expression Error", tokens[max_operator].file_info)

def _statement_sa(tokens: list[lexer.Token]) -> Statement:
    token = tokens.pop(0)
    if isinstance(token, lexer.Keyword):
        match token.value:
            case 'let' | 'static' as key:
                static = key == 'static'
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
                    Identifier(identifier.value),
                    data_type,
                    pointer,
                    static,
                    literal,
                )
            case 'break' | 'continue' as key:
                token = tokens.pop(0)
                _assert_token(ExpectedPunctuation, token, ';')
                return LoopStatements(key)
            case 'if':
                condition = _expression_sa(_get_nested_group(tokens))
                code = _code_block_sa(tokens)
                if tokens[0].value == 'else':
                    else_block = ElseBlock(_code_block_sa(tokens))
                else:
                    else_block = None
                return IfBlock(condition, code, else_block)
            case 'do':
                code1 = _code_block_sa(tokens)
                token = tokens.pop(0)
                _assert_token(ExpectedKeyword, token, 'while')
                condition = _expression_sa(_get_nested_group(tokens))
                if tokens[0].value == '{':
                    code2 = _code_block_sa(tokens)
                else:
                    code2 = None
                if tokens[0].value == 'else':
                    else_block = ElseBlock(_code_block_sa(tokens))
                else:
                    else_block = None
                return DoBlock(code1, condition, code2, else_block)
            case 'while':
                condition = _expression_sa(_get_nested_group(tokens))
                code = _code_block_sa(tokens)
                if tokens[0].value == 'else':
                    else_block = ElseBlock(_code_block_sa(tokens))
                else:
                    else_block = None
                return WhileBlock(condition, code, else_block)
            case 'for':
                three_expressions = _get_nested_group(tokens)
                token = three_expressions.pop(0)
                pre_loop_tokens: list[lexer.Token] = []
                while token.value != ';':
                    pre_loop_tokens.append(token)
                    token = three_expressions.pop(0)
                token = three_expressions.pop(0)
                if (
                    type(pre_loop_tokens[0]) is lexer.Identifier and
                    pre_loop_tokens[1].value == ':'
                ):
                    identifier = Identifier(pre_loop_tokens.pop(0).value)
                    token = pre_loop_tokens.pop(0)
                    _assert_token(ExpectedPunctuation, token, ':')
                    pointer, data_type = _data_type_sa(pre_loop_tokens)
                    if pre_loop_tokens:
                        token = pre_loop_tokens.pop(0)
                        _assert_token(ExpectedPunctuation, token, '=')
                        pre_loop_expr = _expression_sa(pre_loop_tokens)
                    pre_loop = ForPreDef(
                        identifier,
                        data_type,
                        pointer,
                        pre_loop_expr,
                    )
                else:
                    pre_loop = _expression_sa(pre_loop_tokens)
                loop_condition_tokens: list[lexer.Token] = []
                while token.value != ';':
                    loop_condition_tokens.append(token)
                    token = three_expressions.pop(0)
                token = three_expressions.pop(0)
                condition = _expression_sa(loop_condition_tokens)
                post_loop = _expression_sa(three_expressions)
                code = _code_block_sa(tokens)
                if tokens[0].value == 'else':
                    else_block = ElseBlock(_code_block_sa(tokens))
                else:
                    else_block = None
                return ForBlock(
                    pre_loop, condition, code, post_loop, else_block)
            case key if key not in BuiltInConst:
                raise UnexpectedKeyword(token, [
                    'static',
                    'let',
                    'break',
                    'continue',
                    'if',
                    'do',
                    'while',
                    'for',
                ] + [i.value for i in BuiltInConst])
    expr_tokens: list[lexer.Token] = [token] + _get_to_symbol(tokens)
    return _expression_sa(expr_tokens)

def _file_sa(tokens: list[lexer.Token]) -> File:
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
                        _struct_sa(tokens))
                case 'enum':
                    children.append(
                        _enumeration_sa(tokens))
                case 'fn':
                    children.append(
                        _function_sa(tokens))
                case _:
                    raise ExpectedKeyword(token, "struct', 'enum', or 'fn")
        else:
            raise UnexpectedToken(token, "directive' or 'keyword")

    return File(children)


def syntactical_analyzer(tokens: Sequence[lexer.Token]) -> File:
    return _file_sa(list(tokens))

