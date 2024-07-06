# Kyler Olsen
# Mar 2024

from enum import Enum
from typing import ClassVar

from .compiler_types import CompilerError, FileInfo
from . import syntactical_analyzer


type SymbolDefinitionTypes = (
    InternalDefinition |
    syntactical_analyzer.FunctionParameter |
    syntactical_analyzer.LetStatement |
    syntactical_analyzer.ForPreDef |
    syntactical_analyzer.StructBlock |
    FunctionBlock |
    syntactical_analyzer.EnumBlock |
    FunctionReturnDefinition
)


type SymbolReferenceTypes = (
    syntactical_analyzer.Identifier |
    syntactical_analyzer.StructBlock |
    FunctionBlock |
    syntactical_analyzer.EnumBlock
)


type Identifier = (
    syntactical_analyzer.Identifier |
    CompoundIdentifier |
    AddressOfIdentifier |
    DereferenceIdentifier
)


type Statement = (
    syntactical_analyzer.Expression |
    syntactical_analyzer.LetStatement |
    syntactical_analyzer.LoopStatements |
    syntactical_analyzer.NestableCodeBlock |
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


HasOperands: tuple[type, ...] = (
    syntactical_analyzer.UnaryExpression,
    syntactical_analyzer.BinaryExpression,
    syntactical_analyzer.TernaryExpression,
)


AddRefTypes: tuple[type, ...] = (
    syntactical_analyzer.UnaryExpression,
    syntactical_analyzer.BinaryExpression,
    syntactical_analyzer.TernaryExpression,
    syntactical_analyzer.FunctionCall,
    syntactical_analyzer.Identifier,
)


IncrementOperators: tuple[
    syntactical_analyzer.PostfixUnaryOperatorEnum |
    syntactical_analyzer.PrefixUnaryOperatorEnum, ...
] = (
    syntactical_analyzer.PostfixUnaryOperatorEnum.Increment,
    syntactical_analyzer.PostfixUnaryOperatorEnum.Decrement,
    syntactical_analyzer.PrefixUnaryOperatorEnum.Increment,
    syntactical_analyzer.PrefixUnaryOperatorEnum.Decrement,
)


PointerOperators: tuple[syntactical_analyzer.PrefixUnaryOperatorEnum, ...] = (
    syntactical_analyzer.PrefixUnaryOperatorEnum.AddressOf,
    syntactical_analyzer.PrefixUnaryOperatorEnum.Dereference,
)


AssignmentOperators: tuple[syntactical_analyzer.BinaryOperatorEnum, ...] = (
    syntactical_analyzer.BinaryOperatorEnum.Assignment,
    syntactical_analyzer.BinaryOperatorEnum.AdditionAssignment,
    syntactical_analyzer.BinaryOperatorEnum.SubtractionAssignment,
    syntactical_analyzer.BinaryOperatorEnum.MultiplicationAssignment,
    syntactical_analyzer.BinaryOperatorEnum.DivisionAssignment,
    syntactical_analyzer.BinaryOperatorEnum.ModulusAssignment,
    syntactical_analyzer.BinaryOperatorEnum.BitwiseANDAssignment,
    syntactical_analyzer.BinaryOperatorEnum.BitwiseORAssignment,
    syntactical_analyzer.BinaryOperatorEnum.BitwiseXORAssignment,
    syntactical_analyzer.BinaryOperatorEnum.LeftShiftAssignment,
    syntactical_analyzer.BinaryOperatorEnum.RightShiftAssignment,
)


OperandKeys: tuple[str, ...] = ("operand","operand1","operand2","operand3",)


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
        variable: syntactical_analyzer.Identifier,
    ):
        message = (
            f"The variable '{variable.content}' is undeclared."
        )
        super().__init__(message, variable.file_info) # type: ignore


class InvalidOperand(SyntaxError):

    def __init__(
        self,
        operator: (
            syntactical_analyzer.TernaryExpression |
            syntactical_analyzer.BinaryExpression |
            syntactical_analyzer.UnaryExpression |
            syntactical_analyzer.Operator
        ),
        operand: Statement,
    ):
        if isinstance(operator, (
            syntactical_analyzer.TernaryExpression,
            syntactical_analyzer.BinaryExpression,
            syntactical_analyzer.UnaryExpression,
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
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = f"{pre} CompoundIdentifier\n"
        s += f"{pre_cont}├─ Owner\n"
        s += self._owner.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
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
    def file_info(self) -> FileInfo: return self._file_info

    def tree_str(self, pre: str = "", pre_cont: str = "") -> str:
        s: str = (
            f"{pre} Unary Expression: PrefixUnaryOperator.Dereference\n"
        )
        s += self._operand.tree_str(pre_cont + "└─", pre_cont + "  ")
        return s


class InternalDefinition:

    _index: ClassVar[int] = 0

    _identifier: syntactical_analyzer.Identifier
    _operand: syntactical_analyzer.Expression

    def __init__(
        self,
        operand: syntactical_analyzer.Expression,
    ):
        self._identifier = syntactical_analyzer.Identifier(
            f"`{InternalDefinition._index}",
            FileInfo("",0,0,0,0)
        )
        self._operand = operand
        InternalDefinition._index += 1

    @property
    def identifier(self) -> syntactical_analyzer.Identifier:
        return self._identifier

    @property
    def operand(self) -> syntactical_analyzer.Expression:
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
            title_width = name_width + 2 + type_width + 3 + count_width

            s = f"{pre} o{title.center(title_width, '-')}o\n"
            for i in range(len(self._symbols)):
                s += f"{pre_cont} |{(names[i] + ':').ljust(name_width + 1)} "
                s += f"{types[i].value.ljust(type_width)} - "
                s += f"{str(counts[i]).rjust(count_width)}|\n"
            s += f"{pre_cont} o{'-' * title_width}o\n"

            return s
        else: return f"{pre} o-{title}-o\n"


class CodeBlock:

    _parent: BlockHolder
    _code: list[Statement]

    def __init__(self, parent: BlockHolder, code: list[Statement]):
        self._parent = parent
        self._code = code[:]

    def tree_str(
        self,
        pre: str = "",
        pre_cont: str = "",
        cont: bool = False,
    ) -> str:
        s: str = ""
        if self._code:
            if cont: s += f"{pre}├─ Code\n"
            else: s += f"{pre}└─ Code\n"
            for code in self._code[:-1]:
                s += code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
            s += self._code[-1].tree_str(pre_cont + "  └─", pre_cont + "    ")
        return s

    @staticmethod
    def _sa(
        parent: BlockHolder,
        code: list[syntactical_analyzer.Statement],
        symbol_table: SymbolTable,
        members: list[syntactical_analyzer.LetStatement],
    ) -> "CodeBlock":

        def add_ref_if(statement: syntactical_analyzer.Expression):
            if isinstance(statement, HasOperands):
                for key in OperandKeys:
                    if (
                        hasattr(statement, key) and
                        isinstance(
                            getattr(statement, key),
                            syntactical_analyzer.Identifier,
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
                            syntactical_analyzer.FunctionCall,
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
                            syntactical_analyzer.BinaryExpression,
                        ) and
                        (
                            statement.operator ==
                            syntactical_analyzer.BinaryOperatorEnum.Assignment
                        ) and
                        hasattr(statement, key) and
                        isinstance(
                            getattr(statement, key),
                            syntactical_analyzer.BinaryExpression,
                        )
                    ):
                        add_ref_if(getattr(statement, key))
            elif isinstance(statement, syntactical_analyzer.FunctionCall):
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
            elif isinstance(statement, syntactical_analyzer.Identifier):
                try:
                    symbol = symbol_table.get(statement.content)
                except KeyError:
                    raise UndeclaredVariable(statement)
                else:
                    symbol.add_reference(statement)

        code_out: list[Statement] = []
        for root_statement in code:
            for statement in _flatten_statement(root_statement):
                if isinstance(statement, syntactical_analyzer.LetStatement):
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
                    code_out.append(statement)
                else:
                    code_out.append(statement)

        return CodeBlock(parent, code_out)


class FunctionReturnDefinition:

    _identifier: syntactical_analyzer.Identifier
    _return_type_pointer: bool
    _return_type: syntactical_analyzer.DataType | None

    def __init__(
        self,
        identifier: syntactical_analyzer.Identifier,
        return_type_pointer: bool,
        return_type: syntactical_analyzer.DataType | None,
    ):
        self._identifier = identifier
        self._return_type_pointer = return_type_pointer
        self._return_type = return_type

    @property
    def identifier(self) -> syntactical_analyzer.Identifier:
        return self._identifier

    @property
    def return_type_pointer(self) -> bool: return self._return_type_pointer

    @property
    def return_type(self) -> syntactical_analyzer.DataType | None:
        return self._return_type


class FunctionBlock:

    _identifier: syntactical_analyzer.Identifier
    _params: list[syntactical_analyzer.FunctionParameter]
    _return_type: FunctionReturnDefinition
    _members: list[syntactical_analyzer.LetStatement]
    _code: CodeBlock
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        identifier: syntactical_analyzer.Identifier,
        params: list[syntactical_analyzer.FunctionParameter],
        return_type: FunctionReturnDefinition,
        members: list[syntactical_analyzer.LetStatement],
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
    def identifier(self) -> syntactical_analyzer.Identifier:
        return self._identifier

    @property
    def params(self) -> list[syntactical_analyzer.FunctionParameter]:
        return self._params[:]

    @property
    def return_type(self) -> FunctionReturnDefinition: return self._return_type

    @property
    def members(self) -> list[syntactical_analyzer.LetStatement]:
        return self._members[:]

    @property
    def code(self) -> CodeBlock: return self._code

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
        s += self._code.tree_str(pre_cont + "  ├─", pre_cont + "  │ ")
        return s

    @staticmethod
    def _sa(
        func: syntactical_analyzer.FunctionBlock,
        parent_table: SymbolTable,
    ) -> "FunctionBlock":
        symbol_table = SymbolTable(parent_table)
        members: list[syntactical_analyzer.LetStatement] = []

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

        code = CodeBlock._sa(func, func.code, symbol_table, members)

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
            # TODO: analyze structs
            # TODO: analyze enums
            else:
                new_child = child
            children.append(new_child)
        file = File(children, syntax_tree._file_info, symbol_table)
        return file


def _compound_identifier(
    statement: syntactical_analyzer.BinaryExpression,
    operator: syntactical_analyzer.Operator,
) -> CompoundIdentifier:
    if (
        statement.operator.content ==
        syntactical_analyzer.BinaryOperatorEnum.MemberOf
    ): return CompoundIdentifier(
            _assert_identifier(statement.operand1, statement.operator),
            _assert_identifier(statement.operand2, statement.operator),
            statement.file_info,
        )
    else: raise InvalidOperand(operator, statement)

def _augment_identifier(
    statement: syntactical_analyzer.UnaryExpression,
    operator: syntactical_analyzer.Operator,
) -> AddressOfIdentifier | DereferenceIdentifier:
    if (
        statement.operator.content ==
        syntactical_analyzer.PrefixUnaryOperatorEnum.AddressOf
    ): return AddressOfIdentifier(
            _assert_identifier(statement.operand, statement.operator),
            statement.file_info,
        )
    elif (
        statement.operator.content ==
        syntactical_analyzer.PrefixUnaryOperatorEnum.Dereference
    ): return DereferenceIdentifier(
            _assert_identifier(statement.operand, statement.operator),
            statement.file_info,
        )
    else: raise InvalidOperand(operator, statement)

def _assert_identifier(
    statement: syntactical_analyzer.Statement,
    operator: syntactical_analyzer.Operator,
) -> Identifier:
    if isinstance(statement, syntactical_analyzer.Identifier):
        return statement
    elif isinstance(statement, syntactical_analyzer.UnaryExpression):
        return _augment_identifier(statement, operator)
    elif isinstance(statement, syntactical_analyzer.BinaryExpression):
        return _compound_identifier(statement, operator)
    else: raise InvalidOperand(operator, statement)

def _create_internal_definition(
    statement: syntactical_analyzer.Expression,
) -> list[Statement]:
    flattened = _flatten_statement(statement)
    internal_definition = InternalDefinition(
        flattened[-1]) # type: ignore
    return flattened[:-1] + [
        internal_definition, internal_definition.identifier]

def _flatten_statement(
    statement: syntactical_analyzer.Statement,
) -> list[Statement]:

    if isinstance(statement, syntactical_analyzer.UnaryExpression):
        if statement.operator.content in IncrementOperators:
            return [syntactical_analyzer.UnaryExpression(
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
                syntactical_analyzer.UnaryExpression(
                    statement.operator,
                    flattened[-1], # type: ignore
                    statement.file_info,
                )
            ]

    elif isinstance(statement, syntactical_analyzer.BinaryExpression):
        if (
            statement.operator.content ==
            syntactical_analyzer.BinaryOperatorEnum.MemberOf
        ): return [CompoundIdentifier(
            _assert_identifier(statement.operand1, statement.operator),
            _assert_identifier(statement.operand2, statement.operator),
            statement.file_info,
        )]
        elif (
            statement.operator.content ==
            syntactical_analyzer.BinaryOperatorEnum.Assignment
        ):
            flattened = _flatten_statement(statement.operand2)
            return flattened[:-1] + [syntactical_analyzer.BinaryExpression(
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
                return [syntactical_analyzer.BinaryExpression(
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
                return flattened[:-1] + [syntactical_analyzer.BinaryExpression(
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
                syntactical_analyzer.BinaryExpression(
                    statement.operator,
                    flattened1[-1], # type: ignore
                    flattened2[-1], # type: ignore
                    statement.file_info,
                )
            ]

    elif isinstance(statement, syntactical_analyzer.TernaryExpression):
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
            syntactical_analyzer.TernaryExpression(
                statement.operator,
                flattened1[-1], # type: ignore
                flattened2[-1], # type: ignore
                flattened3[-1], # type: ignore
                statement.file_info,
            )
        ]

    else: return [statement]

def semantical_analyzer(syntax_tree: syntactical_analyzer.File) -> File:
    return File._sa(syntax_tree)
