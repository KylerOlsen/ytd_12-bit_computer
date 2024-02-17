# Kyler Olsen
# Feb 2024

from collections import namedtuple


class AssemblerError(Exception): pass
class LinkerError(Exception): pass


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


class Label:

    value: str

    def __init__(self, value: str):
        self.value = value


class Immediate(Label): pass


class Program:

    _instructions: list[Instruction | Label]
    _labels: list[tuple[int, Label]]
    _immediate: list[tuple[int, Immediate]]

    def __init__(self, instructions: list[Instruction | Label]):
        self._instructions = instructions
        self._labels = []
        self._immediate = []
        for index, item in enumerate(self._instructions):
            if isinstance(item, Label) and not isinstance(item, Immediate):
                self._labels.append((index, item))
            elif isinstance(item, Immediate):
                self._immediate.append((index, item))

    def __bytes__(self) -> bytes:
        if self._labels or self._immediate:
            raise LinkerError("Program Not Linked Properly.")
        for item in self._instructions:
            if not isinstance(item, Instruction):
                raise LinkerError("Program Not Linked Properly.")

        output = bytearray()
        for i in self._instructions:
            output += bytes(i) # type: ignore
        return output

    def link(self):
        pass

def reg(reg: str) -> int:
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
        raise AssemblerError(f"Invalid Register: {reg}")

def reg1(l: str) -> int:
    args = l.split(' ')
    if len(args) == 2:
        return reg(args[1])
    else:
        raise AssemblerError(f"Invalid number of arguments: {args[0]}")

def reg2(l: str) -> tuple[int, int]:
    args = l.split(' ')
    if len(args) == 3:
        return reg(args[2]), reg(args[1])
    else:
        raise AssemblerError(f"Invalid number of arguments: {args[0]}")

def reg3(l: str) -> tuple[int, int, int]:
    args = l.split(' ')
    if len(args) == 4:
        return reg(args[2]), reg(args[3]), reg(args[1])
    else:
        raise AssemblerError(f"Invalid number of arguments: {args[0]}")

def immediate(l: str) -> Instruction | Immediate:
    args = l.split(' ')
    if len(args) == 2:
        if ':' in args[1]:
            return Immediate(args[1][1:])
        elif 'b' in args[1]:
            value = int(args[1].split('b')[1], base=2)
        elif 'o' in args[1]:
            value = int(args[1].split('o')[1], base=8)
        elif 'x' in args[1]:
            value = int(args[1].split('x')[1], base=16)
        else:
            value = int(args[1])

        return Instruction(
            0,
            2 + ((value & 0x040) >> 6),
            (value & 0x038) >> 3,
            value & 0x007,
        )
    else:
        raise AssemblerError(f"Invalid number of arguments: {args[0]}")

def parse(s: str) -> list[Instruction | Label]:
    instruction_set = {
        "NOP": lambda _: Instruction(0,0,0,0),
        "HLT": lambda _: Instruction(0,0,0,1),
        "INT": lambda _: Instruction(0,0,0,2),
        "BNZ": lambda _: Instruction(0,0,0,3),
        "BLK": lambda _: Instruction(0,0,0,4),
        "ENB": lambda _: Instruction(0,0,0,5),

        "GLA": lambda l: Instruction(0,0,2,reg1(l)),
        "GET": lambda l: Instruction(0,0,3,reg1(l)),
        "LOD": lambda l: Instruction(0,0,4,reg1(l)),
        "STR": lambda l: Instruction(0,0,5,reg1(l)),
        "PSH": lambda l: Instruction(0,0,6,reg1(l)),
        "POP": lambda l: Instruction(0,0,7,reg1(l)),

        "LDI": lambda l: immediate(l),

        "LSH": lambda l: Instruction(0,4,*reg2(l)),
        "RSH": lambda l: Instruction(0,5,*reg2(l)),
        "INC": lambda l: Instruction(0,6,*reg2(l)),
        "DEC": lambda l: Instruction(0,7,*reg2(l)),

        "AND": lambda l: Instruction(1,*reg3(l)),
        "OR":  lambda l: Instruction(2,*reg3(l)),
        "NAD": lambda l: Instruction(3,*reg3(l)),
        "SUB": lambda l: Instruction(4,*reg3(l)),
        "XOR": lambda l: Instruction(5,*reg3(l)),
        "NOR": lambda l: Instruction(6,*reg3(l)),
        "ADD": lambda l: Instruction(7,*reg3(l)),
    }
    instructions = []

    for rl in s.splitlines(False):
        l = rl.strip()
        if l[0] == ";":
            pass
        elif l[:3] in instruction_set:
            instructions.append(instruction_set[l[:3]](l))
        elif l[:2] in instruction_set:
            instructions.append(instruction_set[l[:2]](l))
        elif l[-1] == ":":
            instructions.append(Label(l[:-1]))
        elif l.strip():
            raise AssemblerError(f"Invalid Instruction: '{l.strip()}'")

    return instructions
