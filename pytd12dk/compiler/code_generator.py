# Kyler Olsen
# Jul 2024

from datetime import datetime

from .compiler_types import CompilerError
from . import syntactical_analyzer as sya
from . import semantical_analyzer as sma

CODE = (0x000, 0x6ff)
IO = (0x700, 0x7ff)
RAM = (0x800, 0xfff)


class CodeGenerationError(Exception): pass


class CodeGenerationNotImplemented(CompilerError):

    _compiler_error_type = "Code Generation"


class _State:

    memory: dict[sma.Symbol, int]
    local: dict[sma.Symbol, int]
    registers: dict[str, sma.Symbol | bool]
    _register_rotation: int
    _loop_index: int

    def __init__(self):
        self.memory = dict()
        self.local = dict()
        self.registers = {
            'D0': False,
            'D1': False,
            'D2': False,
            'D3': False,
        }
        self._register_rotation = 0
        self._loop_index = 0

    @property
    def register_rotation(self) -> str:
        for reg in self.registers:
            if self.registers[reg] is False:
                self._register_rotation = (int(reg[1]) + 1) % 4
                return reg
        else:
            try: return f"D{self._register_rotation}"
            finally:
                self._register_rotation += 1
                self._register_rotation %= 4

    @property
    def loop_index(self) -> str:
        self._loop_index += 1
        return f"`loop{self._loop_index - 1}"

    def store_symbol(self, reg: str) -> str:
        code = ""
        if isinstance(self.registers[reg], sma.Symbol):
            symbol = self.registers[reg]
            if symbol in self.local:
                code += f"ldi {self.local[symbol]}\n"
                code += "add MP SP MP\n"
                code += f"str {reg}\n"
            elif symbol in self.memory:
                code += f"ldi {self.memory[symbol]}\n"
                code += f"str {reg}\n"
        self.registers[reg] = False
        return code

    def load_symbol(self, symbol: sma.Symbol, reg: str | None = None) -> str:
        code = ""
        if reg is None:
            reg = self.register_rotation
        if isinstance(self.registers[reg], sma.Symbol):
            self.store_symbol(reg)
        self.registers[reg] = symbol
        if symbol in self.local:
            code += f"ldi {self.local[symbol]}\n"
            code += "add MP SP MP\n"
            code += f"lod {reg}\n"
        elif symbol in self.memory:
            code += f"ldi {self.memory[symbol]}\n"
            code += f"lod {reg}\n"
        else: raise CodeGenerationError(
            f"Can not find memory of symbol: {symbol.name} ({hash(symbol)})")
        return code

    def get_symbol(self, symbol: sma.Symbol) -> str:
        for sym in self.registers.values():
            if sym == symbol:
                return ""
        else:
            return self.load_symbol(symbol)

    def get_register(self, symbol: sma.Symbol) -> str:
        for reg, sym in self.registers.items():
            if sym == symbol:
                return reg
        return "NN"

    def load_immediate(self, value: int) -> str:
        if value >= 64:
            valuea = value // 64
            valueb = value % 64
            return f"liu {valuea}\nlil {valueb}\n"
        else:
            return f"ldi {value}\n"

    def gen_binary_exprs(
        self,
        expression: sya.BinaryExpression,
        symbols: sma.SymbolTable,
        reg: str | None = None,
    ) -> str:
        code = ""
        if expression.operator == sya.BinaryOperatorEnum.Addition:
            if reg:
                if isinstance(expression.operand1, sya.Identifier):
                    code += self.get_symbol(
                        symbols.get(expression.operand1.content))
                    rega = self.get_register(
                        symbols.get(expression.operand1.content))
                elif isinstance(expression.operand1, (
                    sya.BuiltInConst,
                    sya.CharLiteral,
                    sya.NumberLiteral,
                )):
                    rega = self.register_rotation
                    code += f"ldi {expression.operand1.value}\n"
                    code += f"or {rega} MP ZR\n"

                if isinstance(expression.operand2, sya.Identifier):
                    code += self.get_symbol(
                        symbols.get(expression.operand2.content))
                    regb = self.get_register(
                        symbols.get(expression.operand2.content))
                elif isinstance(expression.operand2, (
                    sya.BuiltInConst,
                    sya.CharLiteral,
                    sya.NumberLiteral,
                )):
                    regb = self.register_rotation
                    code += self.load_immediate(expression.operand2.value)
                    code += f"or {regb} MP ZR\n"

                code += f"add {reg} {rega} {regb}\n"
        elif expression.operator == sya.BinaryOperatorEnum.Subtraction:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for Subtraction",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.Multiplication:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for Multiplication",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.Division:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for Division",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.Modulus:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for Modulus",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseAND:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseAND",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseOR:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseOR",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseXOR:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseXOR",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.LeftShift:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for LeftShift",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.RightShift:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for RightShift",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.MemberOf:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for MemberOf",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.Assignment:
            code += self.get_symbol(
                symbols.get(expression.operand1.content)) # type: ignore
            reg = self.get_register(
                symbols.get(expression.operand1.content)) # type: ignore
            if isinstance(expression.operand2, sya.BinaryExpression):
                code += self.gen_binary_exprs(expression.operand2, symbols, reg)
            elif isinstance(expression.operand2, sya.Identifier):
                code += self.get_symbol(
                    symbols.get(expression.operand2.content))
                rega = self.get_register(
                    symbols.get(expression.operand2.content))
                code += f"or {reg} {rega} ZR\n"
            elif isinstance(expression.operand2, (
                sya.BuiltInConst,
                sya.CharLiteral,
                sya.NumberLiteral,
            )):
                regb = self.register_rotation
                code += self.load_immediate(expression.operand2.value)
                code += f"or {reg} MP ZR\n"
        elif expression.operator == sya.BinaryOperatorEnum.AdditionAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for AdditionAssignment",
                expression.file_info
            )
        elif (
            expression.operator ==
            sya.BinaryOperatorEnum.SubtractionAssignment
        ):
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for SubtractionAssignment",
                expression.file_info
            )
        elif (
            expression.operator ==
            sya.BinaryOperatorEnum.MultiplicationAssignment
        ):
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for MultiplicationAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.DivisionAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for DivisionAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.ModulusAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for ModulusAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseANDAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseANDAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseORAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseORAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BitwiseXORAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BitwiseXORAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.LeftShiftAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for LeftShiftAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.RightShiftAssignment:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for RightShiftAssignment",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BooleanAND:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BooleanAND",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BooleanOR:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BooleanOR",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.BooleanXOR:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for BooleanXOR",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.EqualityComparison:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for EqualityComparison",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.InequalityComparison:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for InequalityComparison",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.LessThan:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for LessThan",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.LessOrEqualToThan:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for LessOrEqualToThan",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.GreaterThan:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for GreaterThan",
                expression.file_info
            )
        elif expression.operator == sya.BinaryOperatorEnum.GreaterOrEqualToThan:
            raise CodeGenerationNotImplemented(
                "Code Generation not implemented for GreaterOrEqualToThan",
                expression.file_info
            )
        return code

    def gen_block(self, block: sma.CodeBlock, symbols: sma.SymbolTable) -> str:
        code = ""
        for statement in block.code:
            if isinstance(statement, sya.LetStatement): pass
            elif isinstance(statement, sya.BinaryExpression):
                code += self.gen_binary_exprs(statement, symbols)
            elif isinstance(statement, sma.WhileBlock):
                code += self.gen_while(statement, symbols)
            else:
                raise CodeGenerationNotImplemented(
                    "Code Generation not yet implemented for: "
                    f"{statement.__class__.__name__}.",
                    statement.file_info, # type: ignore
                )
        return code

    def gen_while(self, loop: sma.WhileBlock, symbols: sma.SymbolTable) -> str:
        start_label = self.loop_index
        end_label = self.loop_index
        break_label = self.loop_index
        code = f"{start_label}:\n"
        if not (
            loop.condition.code and
            isinstance(loop.condition.code[0], sya.BuiltInConst) and
            loop.condition.code[0].content == sya.BuiltInConstEnum.ConstTrue
        ):
            raise CodeGenerationNotImplemented(
                "Code Generation not yet implemented for: "
                "while loop non-true conditions.",
                loop.file_info,
            )
        code += self.gen_block(loop.code, symbols)
        code += f"ldi :{start_label}\nor PC MP ZR\n{end_label}:\n"
        if loop.else_block is not None:
            code += self.gen_block(loop.else_block.code, symbols)
        code += f"{break_label}:\n"

        return code

    def gen_func(self, func: sma.FunctionBlock) -> str:
        self.local = dict()
        memory = 0
        for symbol in func.symbol_table.symbols:
            self.local[symbol] = memory
            memory += 1
        code = f"{func.identifier.content}:\n"
        code += f"\n; Initializing stack for function:"
        code += f" {func.identifier.content}\nldi {memory}\n"
        code += "sub SP SP MP\n\n"

        for symbol in func.symbol_table.symbols:
            if (
                isinstance(symbol.definition, sya.LetStatement) and
                symbol.definition.assignment is not None
            ):
                if isinstance(symbol.definition.assignment, sya.StringLiteral):
                    raise CodeGenerationNotImplemented(
                        "Code Generation not yet implemented for "
                        "loading string literals",
                        symbol.definition.assignment.file_info,
                    )
                else:
                    code += f"; Loading initial value for {symbol.name}\n"
                    code += self.load_immediate(
                        symbol.definition.assignment.value)
                    code += "or D0 MP ZR\n"
                    code += f"ldi {self.local[symbol]}\n"
                    code += "add MP SP MP\n"
                    code += "str D0\n"

        code += self.gen_block(func.code, func.symbol_table)

        code += "\n; Uninitializing stack for function:"
        code += f" {func.identifier.content}\nldi {memory}\n"
        code += "add SP SP MP\n"

        return code

    def code_generator(self, syntax_tree: sma.File, entry_name: str) -> str:
        memory = RAM[0]
        for symbol in syntax_tree.symbol_table.symbols:
            if symbol.symbol_type == sma.SymbolType.variable:
                self.memory[symbol] = memory
                memory += 1 #symbol.definition.size

        code = "; Generated by `pytd12dk` compiler\n"
        code += f"; {datetime.now().isoformat()}\n"
        code += "; Global variables use "
        code += f"{memory - RAM[0]}/{RAM[1] - RAM[0]} bytes\n"
        code += "\n.0x0\n"
        code += self.load_immediate(RAM[1])
        code += f"or SP MP ZR\nldi :{entry_name}\nor PC MP ZR\n"

        for child in syntax_tree.children:
            if isinstance(child, sma.FunctionBlock):
                code += f"\n{self.gen_func(child)}\n"
            else:
                raise CodeGenerationNotImplemented(
                    "Code Generation not yet implemented for: "
                    f"{child.__class__.__name__}.",
                    child.file_info,
                )

        return code

def code_generator(syntax_tree: sma.File, entry_name: str = 'main') -> str:
    return _State().code_generator(syntax_tree, entry_name)