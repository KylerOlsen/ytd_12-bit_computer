# Kyler Olsen
# Feb 2024

from collections import namedtuple
from typing import TypeVar, Generic, Iterable, Sequence

INSTRUCTIONS_COUNT = 0x700

class AssemblerError(Exception): pass
class LinkerError(Exception): pass

KEY = TypeVar("KEY")
ANTIKEY = TypeVar("ANTIKEY")


class TwoWayDictionary(Generic[KEY, ANTIKEY]):

    _dict: dict[KEY, ANTIKEY]
    _antidict: dict[ANTIKEY, KEY]

    def __init__(
        self,
        keys: Iterable[KEY] | None = None,
        antikeys: Iterable[ANTIKEY] | None = None,
    ):
        if (keys is None) and (antikeys is None):
            self._dict = {}
            self._antidict = {}
        elif (
            (keys is None) or
            (antikeys is None) or
            len(keys) != len(antikeys) # type: ignore
        ):
            raise ValueError
        else:
            self._dict = dict(zip(keys, antikeys)) # type: ignore
            self._antidict = dict(zip(antikeys, keys)) # type: ignore

    def get_forwards(self, key: KEY, default: None | ANTIKEY = None) -> ANTIKEY:
        if key not in self._dict:
            if default is None: raise KeyError("Key not in dictionary")
            else: return default
        else: return self._dict[key]

    def get_backwards(
        self,
        antikey: ANTIKEY,
        default: None | KEY = None,
    ) -> KEY:
        if antikey not in self._antidict:
            if default is None: raise KeyError("Anti-Key not in dictionary")
            else: return default
        else: return self._antidict[antikey]

    def set_forwards(self, key: KEY, antikey: ANTIKEY):
        if antikey in self._antidict:
            raise KeyError("Anti-Key already in dictionary.")
        if key in self._dict:
            del self._antidict[self._dict[key]]
        self._dict[key] = antikey
        self._antidict[antikey] = key

    def set_backwards(self, antikey: ANTIKEY, key: KEY):
        if key in self._dict:
            raise KeyError("Key already in dictionary.")
        if antikey in self._antidict:
            del self._dict[self._antidict[antikey]]
        self._antidict[antikey] = key
        self._dict[key] = antikey

    def del_forwards(self, key: KEY):
        if key not in self._dict:
            raise KeyError("Key not in dictionary.")
        del self._antidict[self._dict[key]]
        del self._dict[key]

    def del_backwards(self, antikey: ANTIKEY):
        if antikey not in self._antidict:
            raise KeyError("Anti-Key not in dictionary.")
        del self._dict[self._antidict[antikey]]
        del self._antidict[antikey]

    def keys(self) -> Iterable[KEY]:
        return self._dict.keys()

    def antikeys(self) -> Iterable[ANTIKEY]:
        return self._antidict.keys()

    def items(self) -> Iterable[tuple[KEY, ANTIKEY]]:
        return self._dict.items()

    def antiitems(self) -> Iterable[tuple[ANTIKEY, KEY]]:
        return self._antidict.items()


class Instruction(namedtuple('Instruction', ['bb', 'bl', 'lb', 'll'])):

    def __int__(self) -> int:
        return (
            (self.bb << 9) +
            (self.bl << 6) +
            (self.lb << 3) +
            (self.ll)
        )

    def __bytes__(self) -> bytes:
        value = int(self)
        u = value & 0xf00 >> 8
        m = value & 0xf0 >> 4
        l = value & 0xf
        return bytes((u, m, l))

    def oct_str(self) -> str:
        return (
            str(self.bb) +
            str(self.bl) +
            str(self.lb) +
            str(self.ll)
        )


class Directive:

    @staticmethod
    def directive(line: str, line_number: int) -> "Directive":
        value = int(line[1:], base=0)
        return MemoryLocation(value)


class MemoryLocation(Directive):

    _value: int

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class Label(Directive):

    _value: str

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Immediate(Directive):

    _value: str

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Program:

    instruction_set = {
        "NOP": lambda *_: Instruction(0, 0, 0, 0),
        "HLT": lambda *_: Instruction(0, 0, 0, 1),
        "INT": lambda *_: Instruction(0, 0, 0, 2),
        "BNZ": lambda *_: Instruction(0, 0, 0, 3),
        "BLK": lambda *_: Instruction(0, 0, 0, 4),
        "ENB": lambda *_: Instruction(0, 0, 0, 5),

        "GLA": lambda l, i: Instruction(0, 0, 2, reg1(l, i)),
        "GET": lambda l, i: Instruction(0, 0, 3, reg1(l, i)),
        "LOD": lambda l, i: Instruction(0, 0, 4, reg1(l, i)),
        "STR": lambda l, i: Instruction(0, 0, 5, reg1(l, i)),
        "PSH": lambda l, i: Instruction(0, 0, 6, reg1(l, i)),
        "POP": lambda l, i: Instruction(0, 0, 7, reg1(l, i)),

        "LDI": lambda l, i: immediate(l, i),

        "LSH": lambda l, i: Instruction(0, 4, *reg2(l, i)),
        "RSH": lambda l, i: Instruction(0, 5, *reg2(l, i)),
        "INC": lambda l, i: Instruction(0, 6, *reg2(l, i)),
        "DEC": lambda l, i: Instruction(0, 7, *reg2(l, i)),

        "AND": lambda l, i: Instruction(1, *reg3(l, i)),
        "OR":  lambda l, i: Instruction(2, *reg3(l, i)),
        "NAD": lambda l, i: Instruction(3, *reg3(l, i)),
        "SUB": lambda l, i: Instruction(4, *reg3(l, i)),
        "XOR": lambda l, i: Instruction(5, *reg3(l, i)),
        "NOR": lambda l, i: Instruction(6, *reg3(l, i)),
        "ADD": lambda l, i: Instruction(7, *reg3(l, i)),
    }

    _program: str
    _instructions: list[tuple[int, Instruction | Directive]]
    _immediate: list[tuple[int, Immediate]]

    _instruction_map: TwoWayDictionary[int, int]
    _label_map: dict[str, int]

    def __init__(self, program: str):
        self._program = program

        self._instructions = self.parse(self._program)
        self._immediate = []
        self._label_map = {}
        self._instruction_map = TwoWayDictionary()

        self._link()

    def __bytes__(self) -> bytes:
        output = bytearray()
        for i in range(INSTRUCTIONS_COUNT):
            instruction = self._get_instruction(i)
            output += bytes(instruction)
        return bytes(output)

    def labels(self) -> dict[str, int]:
        return self._label_map.copy()

    def _get_instruction(self, index: int) -> Instruction:
        new_index = self._instruction_map.get_forwards(index, -1)
        if new_index == -1: value = self.instruction_set["NOP"]("NOP", -1)
        else: _, value = self._instructions[new_index]
        if isinstance(value, Immediate):
            return self.instruction_set["LDI"](
                f"LDI {self._label_map[value.value]}", -1)
        elif isinstance(value, Directive):
            raise LinkerError("Unexpected directive!")
        else:
            return value

    def _get_instruction_line(self, index: int) -> int:
        return self._instruction_map.get_backwards(index)

    def _link(self):
        instruction_line = 0
        for index, (line_number, item) in enumerate(self._instructions):
            if isinstance(item, MemoryLocation):
                instruction_line = item.value
            elif isinstance(item, Label):
                if item.value in self._label_map:
                    raise LinkerError(
                        "Label already declared on line"
                        f" {line_number}: {item.value}"
                    )
                self._label_map[item.value] = instruction_line
            elif isinstance(item, Immediate):
                self._immediate.append((index, item))
                self._instruction_map.set_forwards(instruction_line, index)
                instruction_line += 1
            elif isinstance(item, Directive):
                raise LinkerError(
                    f"Unknown or Invalid Directive! on line {line_number}.")
            else:
                self._instruction_map.set_forwards(instruction_line, index)
                instruction_line += 1

    @classmethod
    def parse(cls, s: str) -> list[tuple[int, Instruction | Directive]]:
        instructions: list[tuple[int, Instruction | Directive]] = []

        last_error = None

        for raw_line_number, raw_line in enumerate(s.splitlines(False)):
            try:
                line_number = raw_line_number + 1
                line = raw_line.strip().upper()
                if len(line) == 0 or line[0] == ";":
                    pass
                elif line[:3] in cls.instruction_set:
                    instructions.append((
                        line_number,
                        cls.instruction_set[line[:3]](line, line_number),
                    ))
                elif line[:2] in cls.instruction_set:
                    instructions.append((
                        line_number,
                        cls.instruction_set[line[:2]](line, line_number),
                    ))
                elif line[-1] == ":":
                    instructions.append((
                        line_number,
                        Label(line[:-1]),
                    ))
                elif line[0] == ".":
                    instructions.append((
                        line_number,
                        Directive.directive(line, line_number),
                    ))
                elif line:
                    raise AssemblerError(
                        f"Invalid Instruction on line {line_number}: '{line}'")
            except (AssemblerError, LinkerError) as e:
                last_error = e
                print(f"Error:\n\t{e}")
        if last_error is not None:
            raise last_error

        return instructions


def reg(reg: str, line_number: int) -> int:
    register_names = [
        "ZR",
        "PC",
        "SP",
        "MP",
        "D0",
        "D1",
        "D2",
        "D3",
    ]
    register_numbers = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
    ]
    if reg.upper() in register_names:
        return register_names.index(reg.upper())
    elif reg in register_numbers:
        return register_numbers.index(reg)
    else:
        raise AssemblerError(
            f"Invalid Register on line {line_number}: {reg}")

def reg1(line: str, line_number: int) -> int:
    args = line.split(' ')
    if len(args) == 2:
        return reg(args[1], line_number)
    else:
        raise AssemblerError(
            f"Invalid number of arguments on line {line_number}: {args[0]}")

def reg2(line: str, line_number: int) -> tuple[int, int]:
    args = line.split(' ')
    if len(args) == 3:
        return reg(args[2], line_number), reg(args[1], line_number)
    else:
        raise AssemblerError(
            f"Invalid number of arguments on line {line_number}: {args[0]}")

def reg3(line: str, line_number: int) -> tuple[int, int, int]:
    args = line.split(' ')
    if len(args) == 4:
        return (
            reg(args[2], line_number),
            reg(args[3], line_number),
            reg(args[1], line_number),
        )
    else:
        raise AssemblerError(
            f"Invalid number of arguments on line {line_number}: {args[0]}")

def immediate(line: str, line_number: int) -> Instruction | Immediate:
    args = line.split(' ')
    if len(args) == 2:
        if ':' in args[1]:
            return Immediate(args[1][1:])
        else:
            value = int(args[1], base=0)

        return Instruction(
            0,
            2 + ((value & 0x040) >> 6),
            (value & 0x038) >> 3,
            value & 0x007,
        )
    else:
        raise AssemblerError(
            f"Invalid number of arguments on line {line_number}: {args[0]}")

def main(argv: Sequence[str]):
    import argparse
    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Linker and Assembler',
    )
    parser.add_argument('input_file', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output_file', type=argparse.FileType('wb'))
    parser.add_argument('-l', '--labels_file', type=argparse.FileType('w'))

    args = parser.parse_args(argv)

    program = Program(args.input_file.read())

    if args.output_file:
        args.output_file.write(bytes(program))

    if args.labels_file:
        for label, location in program.labels().items():
            args.labels_file.write(f"{hex(location)}, {label}\n")

if __name__ == '__main__':
    from sys import argv
    main(argv)
