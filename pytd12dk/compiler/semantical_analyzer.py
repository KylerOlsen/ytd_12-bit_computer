# Kyler Olsen
# Mar 2024

from enum import Enum

from .compiler_types import CompilerError, FileInfo
from . import syntactical_analyzer


type SymbolDefinitionTypes = (
    InternalDefinition |
    syntactical_analyzer.FunctionParameter |
    syntactical_analyzer.LetStatement |
    syntactical_analyzer.ForPreDef |
    syntactical_analyzer.StructBlock |
    FunctionBlock |
    syntactical_analyzer.EnumBlock
)


type SymbolReferenceTypes = (
    syntactical_analyzer.Identifier |
    syntactical_analyzer.StructBlock |
    FunctionBlock |
    syntactical_analyzer.EnumBlock
)


type Identifier = syntactical_analyzer.Identifier | CompoundIdentifier


type Statement = (
    syntactical_analyzer.Expression |
    syntactical_analyzer.LetStatement |
    syntactical_analyzer.LoopStatements |
    syntactical_analyzer.NestableCodeBlock |
    Identifier
)


BaseValues: tuple[type, ...] = (
    syntactical_analyzer.BuiltInConst,
    syntactical_analyzer.NumberLiteral,
    syntactical_analyzer.CharLiteral,
    syntactical_analyzer.StringLiteral,
    syntactical_analyzer.Identifier,
    syntactical_analyzer.FunctionCall,
)


NestableCodeBlocks: tuple[type, ...] = (
    syntactical_analyzer.ForBlock,
    syntactical_analyzer.WhileBlock,
    syntactical_analyzer.DoBlock,
    syntactical_analyzer.IfBlock,
)


class SyntaxError(CompilerError):

    _compiler_error_type = "Semantic"


class VariableAlreadyDeclared(SyntaxError):

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


class UndeclaredVariable(SyntaxError):

    def __init__(
        self,
        variable: SymbolDefinitionTypes,
    ):
        message = (
            f"The variable '{variable.identifier.content}' is undeclared."
        )
        super().__init__(message, variable.file_info) # type: ignore


class InvalidOperand(SyntaxError):

    def __init__(
        self,
        operator: (
            syntactical_analyzer.TernaryExpression |
            syntactical_analyzer.BinaryExpression |
            syntactical_analyzer.UnaryExpression
        ),
        operand: Statement,
    ):
        message = (
            f"The operand at '{operand}' is invalid for the "
            f"operator '{operator.operator.content.value}'."
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
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} CompoundIdentifier\n"
        s += f"{pre_cont}├─ Owner\n"
        s += self._owner.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
        s += f"{pre_cont}└─ Member\n"
        s += self._member.tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s


class InternalDefinition:

    _identifier: syntactical_analyzer.Identifier
    _type: syntactical_analyzer.DataType
    _pointer: bool

    def __init__(
        self,
        identifier: syntactical_analyzer.Identifier,
        type: syntactical_analyzer.DataType,
        pointer: bool,
    ):
        self._identifier = identifier
        self._type = type
        self._pointer = pointer

    @property
    def identifier(self) -> syntactical_analyzer.Identifier:
        return self._identifier

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Let Statement: {self._identifier}\n"
        s += pre_cont
        s += '└─ Type: '
        if self._pointer: s+= "@"
        s += f"{self._type}\n"
        return s


class SymbolType(Enum):
    struct = "struct"
    enum = "enum"
    function = "function"
    variable = "variable"


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

    def get(self, key: str) -> Symbol:
        for symbol in self._symbols:
            if symbol.name == key:
                return symbol
        if self._parent_table is None:
            raise KeyError
        else:
            return self._parent_table.get(key)

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
            title_width = name_width + 2 + type_width + 3 + count_width

            s = f"{pre} o{title.center(title_width, '-')}o\n"
            for i in range(len(self._symbols)):
                s += f"{pre_cont} |{(names[i] + ':').ljust(name_width + 1)} "
                s += f"{types[i].value.ljust(type_width)} - "
                s += f"{str(counts[i]).rjust(count_width)}|\n"
            s += f"{pre_cont} o{'-' * title_width}o\n"

            return s
        else: return f"{pre} o-{title}-o\n"


class FunctionBlock:

    _identifier: syntactical_analyzer.Identifier
    _params: list[syntactical_analyzer.FunctionParameter]
    _return_type_pointer: bool
    _return_type: syntactical_analyzer.DataType | None
    _members: list[syntactical_analyzer.LetStatement]
    _code: list[syntactical_analyzer.Statement]
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        identifier: syntactical_analyzer.Identifier,
        params: list[syntactical_analyzer.FunctionParameter],
        return_type_pointer: bool,
        return_type: syntactical_analyzer.DataType | None,
        members: list[syntactical_analyzer.LetStatement],
        code: list[syntactical_analyzer.Statement],
        file_info: FileInfo,
        symbol_table: SymbolTable,
    ):
        self._identifier = identifier
        self._params = params[:]
        self._return_type_pointer = return_type_pointer
        self._return_type = return_type
        self._members = members[:]
        self._code = code[:]
        self._file_info = file_info
        self._symbol_table = symbol_table

    @property
    def identifier(self) -> syntactical_analyzer.Identifier:
        return self._identifier

    @property
    def params(self) -> list[syntactical_analyzer.FunctionParameter]:
        return self._params[:]

    @property
    def return_type_pointer(self) -> bool: return self._return_type_pointer

    @property
    def return_type(self) -> syntactical_analyzer.DataType | None:
        return self._return_type

    @property
    def members(self) -> list[syntactical_analyzer.LetStatement]:
        return self._members[:]

    @property
    def code(self) -> list[syntactical_analyzer.Statement]: return self._code[:]

    @property
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} Function: {self._identifier}\n"
        if (
            self._params or
            self._code or
            self._return_type is not None or
            self._members
        ):
            s += self._symbol_table.table_str(
                self.identifier.content, "├─", "│ ")
        else:
            s += self._symbol_table.table_str(
                self.identifier.content, "└─", "  ")
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
        if self._return_type is not None:
            if self._code or self._members:
                s += f"{pre_cont}├─ Return Type: "
            else:
                s += f"{pre_cont}└─ Return Type: "
            if self._return_type_pointer: s+= "@"
            s += f"{self._return_type}\n"
        if self._members:
            if self._code:
                s += f"{pre_cont}├─ Members: "
            else:
                s += f"{pre_cont}└─ Members: "
            for code in self._members[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._members[-1].tree_str(
                pre_cont + "  └─", pre_cont + "    ")
        if self._code:
            s += f"{pre_cont}└─ Code\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._code[-1].tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s

    @staticmethod
    def _sa(
        func: syntactical_analyzer.FunctionBlock,
        parent_table: SymbolTable,
    ) -> "FunctionBlock":
        symbol_table = SymbolTable(parent_table)
        for param in func.params:
            try:
                symbol_table.add(Symbol(
                    param.identifier.content, SymbolType.variable, param))
            except KeyError:
                raise VariableAlreadyDeclared(
                    param,
                    symbol_table.get(param.identifier.content).definition,
                )
        members: list[syntactical_analyzer.LetStatement] = []
        code: list[syntactical_analyzer.Statement] = []
        for statement in func.code:
            if isinstance(statement, syntactical_analyzer.LetStatement):
                try:
                    symbol_table.add(Symbol(
                        statement.identifier.content,
                        SymbolType.variable, statement,
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
                    code.append(statement)
            else:
                code.append(statement)

        return FunctionBlock(
            func.identifier,
            func.params,
            func.return_type_pointer,
            func.return_type,
            members,
            code,
            func.file_info,
            symbol_table,
        )


class File:

    _children: list[
        syntactical_analyzer.Directive |
        syntactical_analyzer.StructBlock |
        FunctionBlock |
        syntactical_analyzer.EnumBlock
    ]
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        children: list[
            syntactical_analyzer.Directive |
            syntactical_analyzer.StructBlock |
            FunctionBlock |
            syntactical_analyzer.EnumBlock
        ],
        file_info: FileInfo,
        symbol_table: SymbolTable,
    ):
        self._children = children[:]
        self._file_info = file_info
        self._symbol_table = symbol_table

    @property
    def file_info(self) -> FileInfo: return self._file_info

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
    def _sa(syntax_tree: syntactical_analyzer.File) -> "File":
        symbol_table = SymbolTable()
        children: list[
            syntactical_analyzer.Directive |
            syntactical_analyzer.StructBlock |
            FunctionBlock |
            syntactical_analyzer.EnumBlock
        ] = []
        for child in syntax_tree.children:
            symbol: Symbol | None = None
            if isinstance(child, syntactical_analyzer.StructBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.struct,
                    child,
                )
            elif isinstance(child, syntactical_analyzer.FunctionBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.function,
                    child, # type: ignore
                )
            elif isinstance(child, syntactical_analyzer.EnumBlock):
                symbol = Symbol(
                    child.identifier.content,
                    SymbolType.enum,
                    child,
                )
            if symbol is not None:
                symbol_table.add(symbol)
        for child in syntax_tree.children:
            new_child: (
                syntactical_analyzer.Directive |
                syntactical_analyzer.StructBlock |
                FunctionBlock |
                syntactical_analyzer.EnumBlock
            )
            if isinstance(child, syntactical_analyzer.FunctionBlock):
                new_child = FunctionBlock._sa(child, symbol_table)
                symbol_table.get(
                    child.identifier.content
                )._definition = new_child # type: ignore
            else:
                new_child = child
            children.append(new_child)
        file = File(children, syntax_tree._file_info, symbol_table)
        return file


def _get_all_operands(
    expression: syntactical_analyzer.Expression,
) -> list[syntactical_analyzer.Expression]:
    if isinstance(
        expression,
        BaseValues + (
            syntactical_analyzer.LoopStatements,
            syntactical_analyzer.NoOperation,
        ),
    ):
        return [expression]
    elif isinstance(expression, syntactical_analyzer.UnaryExpression):
        return _get_all_operands(expression.operand)
    elif isinstance(expression, syntactical_analyzer.BinaryExpression):
        return (
            _get_all_operands(expression.operand1) +
            _get_all_operands(expression.operand2)
        )
    elif isinstance(expression, syntactical_analyzer.TernaryExpression):
        return (
            _get_all_operands(expression.operand1) +
            _get_all_operands(expression.operand2) +
            _get_all_operands(expression.operand3)
        )

def _flatten_statement(
    statement: syntactical_analyzer.Statement,
) -> list[syntactical_analyzer.Statement]:
    if isinstance(statement, NestableCodeBlocks):
        return [statement]
    elif isinstance(
        statement,
        BaseValues + (
            syntactical_analyzer.LoopStatements,
            syntactical_analyzer.NoOperation,
        ),
    ):
        return [statement]
    elif isinstance(statement, syntactical_analyzer.UnaryExpression):
        if isinstance(statement.operand, BaseValues):
            return [statement]
    elif isinstance(statement, syntactical_analyzer.BinaryExpression):
        if (
            statement.operator.content ==
            syntactical_analyzer.BinaryOperatorEnum.MemberOf
        ):
            pass
    elif isinstance(statement, syntactical_analyzer.TernaryExpression):
        pass

def semantical_analyzer(syntax_tree: syntactical_analyzer.File) -> File:
    return File._sa(syntax_tree)
