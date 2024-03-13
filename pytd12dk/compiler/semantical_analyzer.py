# Kyler Olsen
# Mar 2024

from enum import Enum
from typing import Any

from .compiler_types import CompilerError, FileInfo
from . import syntactical_analyzer


class SymbolType(Enum):
    struct = "struct"
    enum = "enum"
    function = "function"
    builtin = "builtin"
    variable = "variable"


class Symbol:

    _name: str
    _static: bool
    _symbol_type: SymbolType
    _references: list[Any]

    def __init__(self, name: str, symbol_type: SymbolType):
        self._name = name
        self._symbol_type = symbol_type
        self._references = []

    @property
    def name(self) -> str: return self._name

    @property
    def symbol_type(self) -> SymbolType: return self._symbol_type

    @property
    def references(self): return self._references[:]


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


class File:

    _children: list[
        syntactical_analyzer.Directive |
        syntactical_analyzer.StructBlock |
        syntactical_analyzer.FunctionBlock |
        syntactical_analyzer.EnumBlock
    ]
    _file_info: FileInfo
    _symbol_table: SymbolTable

    def __init__(
        self,
        children: list[
            syntactical_analyzer.Directive |
            syntactical_analyzer.StructBlock |
            syntactical_analyzer.FunctionBlock |
            syntactical_analyzer.EnumBlock
        ],
        file_info: FileInfo,
    ):
        self._children = children[:]
        self._file_info = file_info
        self._symbol_table = SymbolTable()

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
        file = File(syntax_tree.children, syntax_tree._file_info)
        for child in file._children:
            symbol: Symbol | None = None
            if isinstance(child, syntactical_analyzer.StructBlock):
                symbol = Symbol(child._identifier._content, SymbolType.struct)
            elif isinstance(child, syntactical_analyzer.FunctionBlock):
                symbol = Symbol(child._identifier._content, SymbolType.function)
            elif isinstance(child, syntactical_analyzer.EnumBlock):
                symbol = Symbol(child._identifier._content, SymbolType.enum)
            if symbol is not None:
                file._symbol_table.add(symbol)
        return file


def semantical_analyzer(syntax_tree: syntactical_analyzer.File) -> File:
    return File._sa(syntax_tree)
