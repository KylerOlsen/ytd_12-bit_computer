# Kyler Olsen
# Feb 2024

from collections import namedtuple

class AssemblerError(Exception): pass

class Instruction(namedtuple('Instruction', ['bb', 'bl', 'lb', 'll'])):

    def __int__(self) -> int:
        return (
            (self.bb << 9) +
            (self.bl << 6) +
            (self.lb << 3) +
            (self.ll)
        )

    def oct_str(self) -> str:
        return (
            str(self.bb) +
            str(self.bl) +
            str(self.lb) +
            str(self.ll)
        )

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

def immediate(l: str) -> Instruction:
    args = l.split(' ')
    if len(args) == 2:
        if 'b' in args[1]:
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

def parse(s: str) -> list[Instruction]:
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
        if l[:3] in instruction_set:
            instructions.append(instruction_set[l[:3]](l))
        elif l[:2] in instruction_set:
            instructions.append(instruction_set[l[:2]](l))

    return instructions
