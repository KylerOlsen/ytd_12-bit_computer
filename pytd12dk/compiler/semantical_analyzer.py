# Kyler Olsen
# Mar 2024

from enum import Enum
from typing import ClassVar

from .compiler_types import CompilerError, FileInfo
from . import syntactical_analyzer as sya


type SymbolDefinitionTypes = (
    InternalDefinition |
    sya.FunctionParameter |
    sya.LetStatement |
    ForPreDef |
    sya.StructBlock |
    FunctionBlock |
    sya.EnumBlock |
    FunctionReturnDefinition
)


type SymbolReferenceTypes = (
    sya.Identifier |
    sya.StructBlock |
    FunctionBlock |
    sya.EnumBlock
)


type Identifier = (
    sya.Identifier |
    CompoundIdentifier |
    AddressOfIdentifier |
    DereferenceIdentifier
)


type NestableCodeBlock = ForBlock | WhileBlock | DoBlock | IfBlock


type IntermediateStatement = (
    sya.Expression |
    sya.LetStatement |
    sya.LoopStatements |
    sya.NestableCodeBlock |
    InternalDefinition |
    Identifier
)


type Statement = (
    sya.Expression |
    sya.LetStatement |
    sya.LoopStatements |
    NestableCodeBlock |
    InternalDefinition |
    Identifier
)


type BlockHolder = (
    ElseBlock |
    ForPreDef |
    ForBlock |
    WhileBlock |
    DoBlock |
    IfBlock |
    FunctionBlock
)


BaseValues: tuple[type, ...] = (
    sya.BuiltInConst,
    sya.NumberLiteral,
    sya.CharLiteral,
    sya.StringLiteral,
    sya.Identifier,
    sya.FunctionCall,
)


NestableCodeBlocks: tuple[type, ...] = (
    sya.ForBlock,
    sya.WhileBlock,
    sya.DoBlock,
    sya.IfBlock,
)


HasOperands: tuple[type, ...] = (
    sya.UnaryExpression,
    sya.BinaryExpression,
    sya.TernaryExpression,
)


AddRefTypes: tuple[type, ...] = (
    sya.UnaryExpression,
    sya.BinaryExpression,
    sya.TernaryExpression,
    sya.FunctionCall,
    sya.Identifier,
)


IncrementOperators: tuple[
    sya.PostfixUnaryOperatorEnum |
    sya.PrefixUnaryOperatorEnum, ...
] = (
    sya.PostfixUnaryOperatorEnum.Increment,
    sya.PostfixUnaryOperatorEnum.Decrement,
    sya.PrefixUnaryOperatorEnum.Increment,
    sya.PrefixUnaryOperatorEnum.Decrement,
)


PointerOperators: tuple[sya.PrefixUnaryOperatorEnum, ...] = (
    sya.PrefixUnaryOperatorEnum.AddressOf,
    sya.PrefixUnaryOperatorEnum.Dereference,
)


AssignmentOperators: tuple[sya.BinaryOperatorEnum, ...] = (
    sya.BinaryOperatorEnum.Assignment,
    sya.BinaryOperatorEnum.AdditionAssignment,
    sya.BinaryOperatorEnum.SubtractionAssignment,
    sya.BinaryOperatorEnum.MultiplicationAssignment,
    sya.BinaryOperatorEnum.DivisionAssignment,
    sya.BinaryOperatorEnum.ModulusAssignment,
    sya.BinaryOperatorEnum.BitwiseANDAssignment,
    sya.BinaryOperatorEnum.BitwiseORAssignment,
    sya.BinaryOperatorEnum.BitwiseXORAssignment,
    sya.BinaryOperatorEnum.LeftShiftAssignment,
    sya.BinaryOperatorEnum.RightShiftAssignment,
)


OperandKeys: tuple[str, ...] = ("operand","operand1","operand2","operand3",)


class SemanticError(CompilerError):

    _compiler_error_type = "Semantic"


class VariableAlreadyDeclared(SemanticError):

    def __init__(
        self,
        new: SymbolDefinitionTypes,
        existing: SymbolDefinitionTypes,
    ):
        message = (
            f"The variable '{new.identifier.content}' was already "
            f"declared at {str(existing.file_info)}" # type: ignore
        )
        super().__init__(message, new.file_info) # type: ignore


class UndeclaredVariable(SemanticError):

    def __init__(
        self,
        variable: sya.Identifier,
    ):
        message = (
            f"The variable '{variable.content}' is undeclared."
        )
        super().__init__(message, variable.file_info) # type: ignore


class InvalidOperand(SemanticError):

    def __init__(
        self,
        operator: (
            sya.TernaryExpression |
            sya.BinaryExpression |
            sya.UnaryExpression |
            sya.Operator
        ),
        operand: IntermediateStatement | Statement,
    ):
        if isinstance(operator, (
            sya.TernaryExpression,
            sya.BinaryExpression,
            sya.UnaryExpression,
        )):
            message = (
                f"The operand at '{operand}' is invalid for the "
                f"operator '{operator.operator.content.value}'."
            )
        else:
            message = (
                f"The operand at '{operand}' is invalid for the "
                f"operator '{operator.content.value}'."
            )
        super().__init__(
            message,
            operand.file_info, # type: ignore
            operator.file_info, # type: ignore
        )


class CompoundIdentifier:

    _owner: Identifier
    _member: Identifier
    _file_info: FileInfo

    def __init__(
        self,
        owner: Identifier,
        member: Identifier,
        file_info: FileInfo,
    ):
        self._owner = owner
        self._member = member
        self._file_info = file_info

    @property
    def owner(self) -> Identifier: return self._owner

    @property
    def member(self) -> Identifier: return self._member

    @property
    def content(self) -> str:
        return self.owner.content + '.' + self.member.content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} CompoundIdentifier\n"
        s += f"{pre_cont}├─ Owner\n"
        s += self._owner.tree_str(pre_cont + "│ └─", pre_cont + "    ")
        s += f"{pre_cont}└─ Member\n"
        s += self._member.tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s


class AddressOfIdentifier:

    _operand: Identifier
    _file_info: FileInfo

    def __init__(
        self,
        operand: Identifier,
        file_info: FileInfo,
    ):
        self._operand = operand
        self._file_info = file_info

    @property
    def operand(self) -> Identifier: return self._operand

    @property
    def content(self) -> str: return self._operand.content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = (
            f"{pre} Unary Expression: PrefixUnaryOperator.AddressOf\n"
        )
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class DereferenceIdentifier:

    _operand: Identifier
    _file_info: FileInfo

    def __init__(
        self,
        operand: Identifier,
        file_info: FileInfo,
    ):
        self._operand = operand
        self._file_info = file_info

    @property
    def operand(self) -> Identifier: return self._operand

    @property
    def content(self) -> str: return self._operand.content

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = (
            f"{pre} Unary Expression: PrefixUnaryOperator.Dereference\n"
        )
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class InternalDefinition:

    _index: ClassVar[int] = 0

    _identifier: sya.Identifier
    _operand: sya.Expression

    def __init__(
        self,
        operand: sya.Expression,
    ):
        self._identifier = sya.Identifier(
            f"`{InternalDefinition._index}",
            FileInfo("",0,0,0,0)
        )
        self._operand = operand
        InternalDefinition._index += 1

    @property
    def identifier(self) -> sya.Identifier:
        return self._identifier

    @property
    def operand(self) -> sya.Expression:
        return self._operand

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Internal Definition: {self._identifier}\n"
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class SymbolType(Enum):
    struct = "struct"
    enum = "enum"
    function = "function"
    variable = "variable"
    return_variable = "return variable"


class Symbol:

    _name: str
    _static: bool
    _symbol_type: SymbolType
    _definition: SymbolDefinitionTypes
    _references: list[SymbolReferenceTypes]

    def __init__(
        self,
        name: str,
        symbol_type: SymbolType,
        definition: SymbolDefinitionTypes,
    ):
        self._name = name
        self._symbol_type = symbol_type
        self._definition = definition
        self._references = []

    def __hash__(self) -> int:
        return id(self)

    @property
    def name(self) -> str: return self._name

    @property
    def symbol_type(self) -> SymbolType: return self._symbol_type

    @property
    def references(self) -> list[SymbolReferenceTypes]:
        return self._references[:]

    @property
    def definition(self) -> SymbolDefinitionTypes: return self._definition

    def add_reference(self, ref: SymbolReferenceTypes):
        self._references.append(ref)


class SymbolTable:

    _parent_table: "SymbolTable | None"
    _symbols: list[Symbol]

    def __init__(self, parent_table: "SymbolTable | None" = None):
        self._parent_table = parent_table
        self._symbols = []

    def __getitem__(self, key: str) -> Symbol: return self.get(key)
    def __setitem__(self, key: str, value: Symbol):
        if key != value.name:
            raise KeyError
        self.set(value)

    @property
    def symbols(self) -> list[Symbol]: return self._symbols[:]

    def get(self, key: str, symbol_type: SymbolType | None = None) -> Symbol:
        for symbol in self._symbols:
            if symbol.name == key and symbol_type is None:
                return symbol
            elif symbol.name == key and symbol.symbol_type == symbol_type:
                return symbol
        if self._parent_table is None:
            raise KeyError
        else:
            return self._parent_table.get(key, symbol_type)

    def set(self, value: Symbol):
        for i, symbol in enumerate(self._symbols):
            if symbol.name == value.name:
                self._symbols[i] = value
                break
        else:
            if self._parent_table is None:
                raise KeyError
            else:
                self._parent_table.set(value)

    def add(self, value: Symbol):
        for symbol in self._symbols:
            if symbol.name == value.name:
                raise KeyError
        else:
            self._symbols.append(value)

    def table_str(self, title: str, pre: str = "", pre_cont: str = "") -> str:
        if len(self._symbols):
            names: list[str] = []
            types: list[SymbolType] = []
            counts: list[int] = []
            for symbol in self._symbols:
                names.append(symbol.name)
                types.append(symbol.symbol_type)
                counts.append(len(symbol.references))
            name_width = max(len(i) for i in names)
            type_width = max(len(i.value) for i in types)
            count_width = max(len(str(i)) for i in counts)
            title_width = name_width + 2 + type_width + 2 + count_width

            s = f"{pre} o{title.center(title_width, '-')}o\n"
            for i in range(len(self._symbols)):
                s += f"{pre_cont} |{(names[i] + ':').ljust(name_width + 1)} "
                s += f"{types[i].value.ljust(type_width)}; "
                s += f"{str(counts[i]).rjust(count_width)}|\n"
            s += f"{pre_cont} o{'-' * title_width}o\n"

            return s
        else: return f"{pre} o-{title}-o\n"


class ForSymbolTable(SymbolTable):

    _parent_table: SymbolTable
    _symbols: list[Symbol]

    def __init__(self, parent_table: SymbolTable):
        self._parent_table = parent_table
        self._symbols = []

    def set(self, value: Symbol): self._parent_table.set(value)

    def add(self, value: Symbol): self._parent_table.add(value)

    def for_add(self, value: Symbol):
        for symbol in self._symbols:
            if symbol.name == value.name:
                raise KeyError
        else:
            self._symbols.append(value)


class CodeBlock:

    _code: list[Statement]

    def __init__(self, code: list[Statement]):
        self._code = code[:]

    @property
    def code(self) -> list[Statement]: return self._code[:]

    def tree_str(
        self,
        pre: str = "",
        pre_cont: str = "",
    ) -> str:
        s: str = ""
        if self._code:
            s += f"{pre} Code Block\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "├─", pre_cont + "│ ")
            s += self._code[-1].tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        code: list[sya.Statement],
        symbol_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "CodeBlock":

        def add_ref_if(statement: sya.Expression):
            if isinstance(statement, HasOperands):
                for key in OperandKeys:
                    if (
                        hasattr(statement, key) and
                        isinstance(
                            getattr(statement, key),
                            sya.Identifier,
                        )
                    ):
                        try:
                            symbol = symbol_table.get(
                                getattr(statement, key).content)
                        except KeyError:
                            raise UndeclaredVariable(getattr(statement, key))
                        else:
                            symbol.add_reference(getattr(statement, key))
                    elif (
                        hasattr(statement, key) and
                        isinstance(
                            getattr(statement, key),
                            sya.FunctionCall,
                        )
                    ):
                        try:
                            symbol = symbol_table.get(
                                getattr(statement, key).identifier.content,
                                SymbolType.function,
                            )
                        except KeyError:
                            raise UndeclaredVariable(
                                getattr(statement, key).identifier)
                        else:
                            symbol.add_reference(
                                getattr(statement, key).identifier)
                        for arg in getattr(statement, key).args:
                            try:
                                symbol = symbol_table.get(arg.value.content)
                            except KeyError:
                                raise UndeclaredVariable(arg.value)
                            else:
                                symbol.add_reference(arg.value)
                    elif (
                        isinstance(
                            statement,
                            sya.BinaryExpression,
                        ) and
                        (
                            statement.operator ==
                            sya.BinaryOperatorEnum.Assignment
                        ) and
                        hasattr(statement, key) and
                        isinstance(
                            getattr(statement, key),
                            sya.BinaryExpression,
                        )
                    ):
                        add_ref_if(getattr(statement, key))
            elif isinstance(statement, sya.FunctionCall):
                try:
                    symbol = symbol_table.get(
                        statement.identifier.content, SymbolType.function)
                except KeyError:
                    raise UndeclaredVariable(statement.identifier)
                else:
                    symbol.add_reference(statement.identifier)
                for arg in statement.args:
                    try:
                        symbol = symbol_table.get(
                            arg.value.content) # type: ignore
                    except KeyError:
                        raise UndeclaredVariable(arg.value) # type: ignore
                    else:
                        symbol.add_reference(arg.value) # type: ignore
            elif isinstance(statement, sya.Identifier):
                try:
                    symbol = symbol_table.get(statement.content)
                except KeyError:
                    raise UndeclaredVariable(statement)
                else:
                    symbol.add_reference(statement)

        code_out: list[Statement] = []
        for root_statement in code:
            for statement in _flatten_statement(root_statement):
                if isinstance(statement, sya.LetStatement):
                    try:
                        symbol_table.add(Symbol(
                            statement.identifier.content,
                            SymbolType.variable,
                            statement,
                        ))
                    except KeyError:
                        raise VariableAlreadyDeclared(
                            statement,
                            symbol_table.get(
                                statement.identifier.content
                            ).definition,
                        )
                    if statement.static:
                        members.append(statement)
                    else:
                        code_out.append(statement)
                elif isinstance(statement, InternalDefinition):
                    add_ref_if(statement.operand)
                    symbol_table.add(Symbol(
                        statement.identifier.content,
                        SymbolType.variable,
                        statement,
                    ))
                    code_out.append(statement)
                elif isinstance(statement, AddRefTypes):
                    add_ref_if(statement) # type: ignore
                    code_out.append(statement) # type: ignore
                elif isinstance(statement, sya.IfBlock):
                    code_out.append(
                        IfBlock._sa(statement, symbol_table, members))
                elif isinstance(statement, sya.DoBlock):
                    code_out.append(
                        DoBlock._sa(statement, symbol_table, members))
                elif isinstance(statement, sya.WhileBlock):
                    code_out.append(
                        WhileBlock._sa(statement, symbol_table, members))
                elif isinstance(statement, sya.ForBlock):
                    code_out.append(
                        ForBlock._sa(statement, symbol_table, members))
                else:
                    code_out.append(statement)

        return CodeBlock(code_out)


class ElseBlock:

    _code: CodeBlock
    _file_info: FileInfo

    def __init__(
        self,
        code: CodeBlock,
        file_info: FileInfo,
    ):
        self._code = code
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def code(self) -> CodeBlock: return self._code

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        return self._code.tree_str(pre + " Else", pre_cont + "")

    @staticmethod
    def _sa(
        else_block: sya.ElseBlock,
        symbol_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "ElseBlock":

        code = CodeBlock._sa(else_block.code, symbol_table, members)

        return ElseBlock(code, else_block.file_info)


class ForPreDef:

    _identifier: Identifier
    _type: sya.DataType
    _pointer: bool
    _assignment: CodeBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        identifier: Identifier,
        type: sya.DataType,
        pointer: bool,
        assignment: CodeBlock | None,
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

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Definition: {self._identifier}\n"
        if self._assignment: s += f"{pre_cont}├─ Type: "
        else: s += f"{pre_cont}└─ Type: "
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        if self._assignment:
            s += self._assignment.tree_str(pre_cont + "└─ Value", pre_cont + "  ")
        return s


class ForBlock:

    _pre_statement: CodeBlock | ForPreDef
    _condition: CodeBlock
    _code: CodeBlock
    _post_statement: CodeBlock
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        pre_statement: CodeBlock | ForPreDef,
        condition: CodeBlock,
        code: CodeBlock,
        post_statement: CodeBlock,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._pre_statement = pre_statement
        self._condition = condition
        self._code = code
        self._post_statement = post_statement
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} For Loop\n"
        s += self._pre_statement.tree_str(
            f"{pre_cont}├─ Pre-Statement", f"{pre_cont}│ ")
        s += self._condition.tree_str(
            f"{pre_cont}├─ Condition", f"{pre_cont}│ ")
        s += self._post_statement.tree_str(
            f"{pre_cont}├─ Post-Statement", f"{pre_cont}│ ")
        if self._else is not None:
            s += self._code.tree_str(
                pre_cont + "├─", pre_cont + "│ ")
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        else:
            s += self._code.tree_str(
                pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        for_block: sya.ForBlock,
        parent_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "ForBlock":
        symbol_table = ForSymbolTable(parent_table)
        if isinstance(for_block.pre_statement, sya.ForPreDef):
            assignment = CodeBlock._sa(for_block.code, symbol_table, members)
            pre_statement = ForPreDef(
                for_block.pre_statement.identifier,
                for_block.pre_statement.data_type,
                for_block.pre_statement.pointer,
                assignment,
                for_block.pre_statement.file_info,
            )
            try: symbol_table.for_add(Symbol(
                    pre_statement.identifier.content,
                    SymbolType.variable,
                    pre_statement,
                ))
            except KeyError: raise VariableAlreadyDeclared(
                pre_statement,
                symbol_table.get(pre_statement.identifier.content).definition,
            )
        else: pre_statement = CodeBlock._sa(
            [for_block.pre_statement], symbol_table, members)
        condition = CodeBlock._sa([for_block.condition], symbol_table, members)
        code = CodeBlock._sa(for_block.code, symbol_table, members)
        post_statement = CodeBlock._sa(
            [for_block.post_statement], symbol_table, members)
        if for_block.else_block is None: else_block = None
        else: else_block = ElseBlock._sa(
            for_block.else_block, symbol_table, members)

        return ForBlock(
            pre_statement,
            condition,
            code,
            post_statement,
            else_block,
            for_block.file_info,
        )


class WhileBlock:

    _condition: CodeBlock
    _code: CodeBlock
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        condition: CodeBlock,
        code: CodeBlock,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._condition = condition
        self._code = code
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def condition(self) -> CodeBlock: return self._condition

    @property
    def code(self) -> CodeBlock: return self._code

    @property
    def else_block(self) -> ElseBlock | None: return self._else

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} While Loop\n"
        if self._code or self._else is not None:
            s += self._condition.tree_str(
                f"{pre_cont}├─ Condition", f"{pre_cont}│ ")
        else:
            s += self._condition.tree_str(
                f"{pre_cont}└─ Condition", f"{pre_cont}  ")
        if self._else is not None:
            s += self._code.tree_str(
                pre_cont + "├─", pre_cont + "│ ")
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        else:
            s += self._code.tree_str(
                pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        while_block: sya.WhileBlock,
        symbol_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "WhileBlock":
        condition = CodeBlock._sa(
            [while_block.condition], symbol_table, members)
        code = CodeBlock._sa(while_block.code, symbol_table, members)
        if while_block.else_block is None: else_block = None
        else: else_block = ElseBlock._sa(
            while_block.else_block, symbol_table, members)

        return WhileBlock(
            condition,
            code,
            else_block,
            while_block.file_info,
        )


class DoBlock:

    _first_code: CodeBlock
    _condition: CodeBlock
    _second_code: CodeBlock | None
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        first_code: CodeBlock,
        condition: CodeBlock,
        second_code: CodeBlock | None,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._first_code = first_code
        self._condition = condition
        if second_code:
            self._second_code = second_code
        else:
            self._second_code = None
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Do Loop\n"
        s += self._first_code.tree_str(
            pre_cont + "├─ First Do", pre_cont + "│ ")
        if self._second_code or self._else is not None:
            s += self._condition.tree_str(
                f"{pre_cont}├─ Condition", f"{pre_cont}│ ")
        else:
            s += self._condition.tree_str(
                f"{pre_cont}└─ Condition", f"{pre_cont}  ")
        if self._second_code is not None:
            if self._else is not None:
                s += self._second_code.tree_str(
                    pre_cont + "├─ Second Do", pre_cont + "│ ")
            else:
                s += self._second_code.tree_str(
                    pre_cont + "└─ Second Do", pre_cont + "  ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        do_block: sya.DoBlock,
        symbol_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "DoBlock":
        condition = CodeBlock._sa([do_block.condition], symbol_table, members)
        first_code = CodeBlock._sa(do_block.first_code, symbol_table, members)
        if do_block.second_code is None: second_code = None
        else: second_code = CodeBlock._sa(
            do_block.second_code, symbol_table, members)
        if do_block.else_block is None: else_block = None
        else: else_block = ElseBlock._sa(
            do_block.else_block, symbol_table, members)

        return DoBlock(
            condition,
            first_code,
            second_code,
            else_block,
            do_block.file_info,
        )


class IfBlock:

    _condition: CodeBlock
    _code: CodeBlock
    _else: ElseBlock | None
    _file_info: FileInfo

    def __init__(
        self,
        condition: CodeBlock,
        code: CodeBlock,
        else_block: ElseBlock | None,
        file_info: FileInfo,
    ):
        self._condition = condition
        self._code = code
        self._else = else_block
        self._file_info = file_info

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} If Statement\n"
        if self._code or self._else is not None:
            s += self._condition.tree_str(
                f"{pre_cont}├─ Condition", f"{pre_cont}│ ")
        else:
            s += self._condition.tree_str(
                f"{pre_cont}└─ Condition", f"{pre_cont}  ")
        s += self._code.tree_str(
            pre_cont + "├─ If", pre_cont + "│ ")
        if self._else is not None:
            s += self._else.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        if_block: sya.IfBlock,
        symbol_table: SymbolTable,
        members: list[sya.LetStatement],
    ) -> "IfBlock":
        condition = CodeBlock._sa([if_block.condition], symbol_table, members)
        code = CodeBlock._sa(if_block.code, symbol_table, members)
        if if_block.else_block is None: else_block = None
        else: else_block = ElseBlock._sa(
            if_block.else_block, symbol_table, members)

        return IfBlock(
            condition,
            code,
            else_block,
            if_block.file_info,
        )


class FunctionReturnDefinition:

    _identifier: sya.Identifier
    _return_type_pointer: bool
    _return_type: sya.DataType | None

    def __init__(
        self,
        identifier: sya.Identifier,
        return_type_pointer: bool,
        return_type: sya.DataType | None,
    ):
        self._identifier = identifier
        self._return_type_pointer = return_type_pointer
        self._return_type = return_type

    @property
    def identifier(self) -> sya.Identifier:
        return self._identifier

    @property
    def return_type_pointer(self) -> bool: return self._return_type_pointer

    @property
    def return_type(self) -> sya.DataType | None:
        return self._return_type


class FunctionBlock:

    _identifier: sya.Identifier
    _params: list[sya.FunctionParameter]
    _return_type: FunctionReturnDefinition
    _members: list[sya.LetStatement]
    _code: CodeBlock
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        identifier: sya.Identifier,
        params: list[sya.FunctionParameter],
        return_type: FunctionReturnDefinition,
        members: list[sya.LetStatement],
        code: CodeBlock,
        file_info: FileInfo,
        symbol_table: SymbolTable,
    ):
        self._identifier = identifier
        self._params = params[:]
        self._return_type = return_type
        self._members = members[:]
        self._code = code
        self._file_info = file_info
        self._symbol_table = symbol_table

    @property
    def identifier(self) -> sya.Identifier:
        return self._identifier

    @property
    def params(self) -> list[sya.FunctionParameter]:
        return self._params[:]

    @property
    def return_type(self) -> FunctionReturnDefinition: return self._return_type

    @property
    def members(self) -> list[sya.LetStatement]:
        return self._members[:]

    @property
    def code(self) -> CodeBlock: return self._code

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def symbol_table(self) -> SymbolTable: return self._symbol_table

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function: {self._identifier}\n"
        if (
            self._params or
            self._code or
            self._return_type is not None or
            self._members
        ):
            s += self._symbol_table.table_str(
                self.identifier.content, pre_cont + "├─", pre_cont + "│ ")
        else:
            s += self._symbol_table.table_str(
                self.identifier.content, pre_cont + "└─", pre_cont + "  ")
        if self._params:
            if self._code or self._return_type is not None or self._members:
                s += f"{pre_cont}├─ Parameters\n"
                params_pre = f"{pre_cont}│ "
            else:
                s += f"{pre_cont}└─ Parameters\n"
                params_pre = f"{pre_cont}  "
            for param in self._params[:-1]:
                s += param.tree_str(params_pre + "├─", params_pre + "│ ")
            s += self._params[-1].tree_str(params_pre + "└─", params_pre + "  ")
        if self.return_type._return_type is not None:
            if self._code or self._members:
                s += f"{pre_cont}├─ Return Type: "
            else:
                s += f"{pre_cont}└─ Return Type: "
            if self.return_type._return_type_pointer: s+= "@"
            s += f"{self.return_type._return_type}\n"
        if self._members:
            if self._code:
                s += f"{pre_cont}├─ Members: "
            else:
                s += f"{pre_cont}└─ Members: "
            for code in self._members[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._members[-1].tree_str(
                pre_cont + "  └─", pre_cont + "    ")
        s += self._code.tree_str(pre_cont + "└─ Function", pre_cont + "  ")
        return s

    @staticmethod
    def _sa(
        func: sya.FunctionBlock,
        parent_table: SymbolTable,
    ) -> "FunctionBlock":
        symbol_table = SymbolTable(parent_table)
        members: list[sya.LetStatement] = []

        function_return = FunctionReturnDefinition(
            func.identifier, func.return_type_pointer, func.return_type)
        if function_return.return_type is not None:
            symbol_table.add(Symbol(
                function_return.identifier.content,
                SymbolType.return_variable,
                function_return,
            ))

        for param in func.params:
            try:
                symbol_table.add(Symbol(
                    param.identifier.content, SymbolType.variable, param))
            except KeyError:
                raise VariableAlreadyDeclared(
                    param,
                    symbol_table.get(param.identifier.content).definition,
                )

        code = CodeBlock._sa(func.code, symbol_table, members)

        return FunctionBlock(
            func.identifier,
            func.params,
            function_return,
            members,
            code,
            func.file_info,
            symbol_table,
        )


class File:

    _children: list[
        sya.Directive |
        sya.StructBlock |
        FunctionBlock |
        sya.EnumBlock
    ]
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        children: list[
            sya.Directive |
            sya.StructBlock |
            FunctionBlock |
            sya.EnumBlock
        ],
        file_info: FileInfo,
        symbol_table: SymbolTable,
    ):
        self._children = children[:]
        self._file_info = file_info
        self._symbol_table = symbol_table

    @property
    def children(self) -> list[
        sya.Directive |
        sya.StructBlock |
        FunctionBlock |
        sya.EnumBlock
    ]: return self._children[:]

    @property
    def file_info(self) -> FileInfo: return self._file_info

    @property
    def symbol_table(self) -> SymbolTable: return self._symbol_table

    def tree_str(self) -> str:
        s: str = " File\n"
        if self._children:
            s += self._symbol_table.table_str("GLOBAL", "├─", "│ ")
            for child in self._children[:-1]:
                s += child.tree_str("├─", "│ ")
            s += self._children[-1].tree_str("└─", "  ")
        else:
            s += self._symbol_table.table_str("GLOBAL", "└─", "  ")
        return s

    @staticmethod
    def _sa(syntax_tree: sya.File) -> "File":
        symbol_table = SymbolTable()
        children: list[
            sya.Directive |
            sya.StructBlock |
            FunctionBlock |
            sya.EnumBlock
        ] = []
        for child in syntax_tree.children:
            symbol: Symbol | None = None
            if isinstance(child, sya.StructBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.struct,
                    child,
                )
            elif isinstance(child, sya.FunctionBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.function,
                    child, # type: ignore
                )
            elif isinstance(child, sya.EnumBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.enum,
                    child,
                )
            if symbol is not None:
                symbol_table.add(symbol)
        for child in syntax_tree.children:
            new_child: sya.StructBlock | FunctionBlock | sya.EnumBlock
            if isinstance(child, sya.FunctionBlock):
                new_child = FunctionBlock._sa(child, symbol_table)
                symbol_table.get(
                    child.identifier.content
                )._definition = new_child # type: ignore
            # TODO: analyze structs
            elif isinstance(child, sya.StructBlock):
                new_child = child
            elif isinstance(child, sya.EnumBlock):
                new_child = _sa_enum(child)
            elif isinstance(child, sya.Directive):
                continue
            children.append(new_child)
        file = File(children, syntax_tree._file_info, symbol_table)
        return file


def _sa_enum(block: sya.EnumBlock) -> sya.EnumBlock:
    members: list[sya.EnumMember] = []
    used_numbers: set[int] = set()
    for member in block.members:
        if member.value is not None:
            used_numbers.add(member.value.value)
    i = 1
    for member in block.members:
        while i in used_numbers:
            i += 1
        if member.value is not None:
            members.append(sya.EnumMember(
                member.identifier,
                member.value,
                member.file_info
            ))
            i = member.value.value + 1
        else:
            used_numbers.add(i)
            members.append(sya.EnumMember(
                member.identifier,
                sya.NumberLiteral(str(i), member.file_info),
                member.file_info
            ))
            i += 1
    return sya.EnumBlock(
        block.identifier,
        sorted(
            sorted(members, key=lambda o: o.identifier.content),
            key=lambda o: o.value.value # type: ignore
        ),
        block.file_info,
    )

def _compound_identifier(
    statement: sya.BinaryExpression,
    operator: sya.Operator,
) -> CompoundIdentifier:
    if (
        statement.operator.content ==
        sya.BinaryOperatorEnum.MemberOf
    ): return CompoundIdentifier(
            _assert_identifier(statement.operand1, statement.operator, True),
            _assert_identifier(statement.operand2, statement.operator, True),
            statement.file_info,
        )
    else: raise InvalidOperand(operator, statement)

def _augment_identifier(
    statement: sya.UnaryExpression,
    operator: sya.Operator,
) -> AddressOfIdentifier | DereferenceIdentifier:
    if (
        statement.operator.content ==
        sya.PrefixUnaryOperatorEnum.AddressOf
    ): return AddressOfIdentifier(
            _assert_identifier(statement.operand, statement.operator, True),
            statement.file_info,
        )
    elif (
        statement.operator.content ==
        sya.PrefixUnaryOperatorEnum.Dereference
    ): return DereferenceIdentifier(
            _assert_identifier(statement.operand, statement.operator, True),
            statement.file_info,
        )
    else: raise InvalidOperand(operator, statement)

def _assert_identifier(
    statement: sya.Statement,
    operator: sya.Operator,
    harsh: bool = False
) -> Identifier:
    if isinstance(statement, sya.Identifier):
        return statement
    elif isinstance(statement, sya.UnaryExpression):
        if (
            isinstance(statement.operand, sya.BinaryExpression)
            and not harsh
        ):
            return statement # type: ignore
        return _augment_identifier(statement, operator)
    elif isinstance(statement, sya.BinaryExpression):
        return _compound_identifier(statement, operator)
    else: raise InvalidOperand(operator, statement)

def _create_internal_definition(
    statement: sya.Expression,
) -> list[IntermediateStatement]:
    flattened = _flatten_statement(statement)
    internal_definition = InternalDefinition(
        flattened[-1]) # type: ignore
    return flattened[:-1] + [
        internal_definition, internal_definition.identifier]

def _flatten_statement(
    statement: sya.Statement,
) -> list[IntermediateStatement]:

    if isinstance(statement, sya.UnaryExpression):
        if statement.operator.content in IncrementOperators:
            return [sya.UnaryExpression(
                statement.operator,
                _assert_identifier( # type: ignore
                    statement.operand, statement.operator),
                statement.file_info,
            )]
        elif statement.operator.content in PointerOperators:
            return [_assert_identifier(statement, statement.operator)]
        elif isinstance(statement.operand, BaseValues):
            return [statement]
        else:
            flattened = _create_internal_definition(statement.operand)
            return flattened[:-1] + [
                sya.UnaryExpression(
                    statement.operator,
                    flattened[-1], # type: ignore
                    statement.file_info,
                )
            ]

    elif isinstance(statement, sya.BinaryExpression):
        if (
            statement.operator.content ==
            sya.BinaryOperatorEnum.MemberOf
        ): return [CompoundIdentifier(
            _assert_identifier(statement.operand1, statement.operator),
            _assert_identifier(statement.operand2, statement.operator),
            statement.file_info,
        )]
        elif (
            statement.operator.content ==
            sya.BinaryOperatorEnum.Assignment
        ):
            flattened = _flatten_statement(statement.operand2)
            return flattened[:-1] + [sya.BinaryExpression(
                statement.operator,
                _assert_identifier( # type: ignore
                    statement.operand1,
                    statement.operator,
                ),
                flattened[-1], # type: ignore
                statement.file_info,
            )]
        elif statement.operator.content in AssignmentOperators:
            if isinstance(statement.operand2, BaseValues):
                return [sya.BinaryExpression(
                    statement.operator,
                    _assert_identifier( # type: ignore
                        statement.operand1,
                        statement.operator,
                    ),
                    statement.operand2,
                    statement.file_info,
                )]
            else:
                flattened = _create_internal_definition(statement.operand2)
                return flattened[:-1] + [sya.BinaryExpression(
                    statement.operator,
                    _assert_identifier( # type: ignore
                        statement.operand1,
                        statement.operator,
                    ),
                    flattened[-1], # type: ignore
                    statement.file_info,
                )]
        else:
            if isinstance(statement.operand1, BaseValues):
                flattened1 = [statement.operand1]
            else: flattened1 = _create_internal_definition(statement.operand1)
            if isinstance(statement.operand2, BaseValues):
                flattened2 = [statement.operand2]
            else: flattened2 = _create_internal_definition(statement.operand2)
            return flattened1[:-1] + flattened2[:-1] + [
                sya.BinaryExpression(
                    statement.operator,
                    flattened1[-1], # type: ignore
                    flattened2[-1], # type: ignore
                    statement.file_info,
                )
            ]

    elif isinstance(statement, sya.TernaryExpression):
        if isinstance(statement.operand1, BaseValues):
            flattened1 = [statement.operand1]
        else: flattened1 = _create_internal_definition(statement.operand1)
        if isinstance(statement.operand2, BaseValues):
            flattened2 = [statement.operand2]
        else: flattened2 = _create_internal_definition(statement.operand2)
        if isinstance(statement.operand3, BaseValues):
            flattened3 = [statement.operand3]
        else: flattened3 = _create_internal_definition(statement.operand3)
        return flattened1[:-1] + flattened2[:-1] + flattened3[:-1] + [
            sya.TernaryExpression(
                statement.operator,
                flattened1[-1], # type: ignore
                flattened2[-1], # type: ignore
                flattened3[-1], # type: ignore
                statement.file_info,
            )
        ]

    else: return [statement]

def semantical_analyzer(syntax_tree: sya.File) -> File:
    return File._sa(syntax_tree)
