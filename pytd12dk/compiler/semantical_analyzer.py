# Kyler Olsen
# Mar 2024

from enum import Enum

from .compiler_types import CompilerError, FileInfo
from . import syntactical_analyzer


class SyntaxError(CompilerError):

    _compiler_error_type = "Semantic"


type SymbolDefinitionTypes = (
    InternalDefinition |
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
    def references(self): return self._references[:]

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
        if self._params or self._code or self._return_type is not None:
            s += self._symbol_table.table_str("GLOBAL", "├─", "│ ")
        else:
            s += self._symbol_table.table_str("GLOBAL", "└─", "  ")
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
    def _sa(
        func: syntactical_analyzer.FunctionBlock,
        parent_table: SymbolTable,
    ) -> "FunctionBlock":
        symbol_table = SymbolTable(parent_table)



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


def semantical_analyzer(syntax_tree: syntactical_analyzer.File) -> File:
    return File._sa(syntax_tree)
