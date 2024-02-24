# Kyler Olsen
# Feb 2024

from typing import BinaryIO

MAX_INT = 0x1000


class Device:

    _start: int
    _end: int

    def __init__(self, start: int, end: int | None = None):
        self._start = start
        self._end = end or start

    def __contains__(self, value: int) -> bool:
        return self._start <= value <= self._end

    def __getitem__(self, index: int) -> int:
        return 0

    def __setitem__(self, index: int, value: int):
        pass


class Memory:

    _rom: list[int]
    _devices: list[Device]
    _ram: list[int]


    def __init__(
        self,
        rom: list[int],
        devices: list[Device] | None = None,
    ) -> None:
        self._rom = [0] * 0x700
        self._devices = (devices or list())[:]
        self._ram = [0] * 0x1000

        for i, data in enumerate(rom):
            self._rom[i] = data % MAX_INT

    def _get_device(self, index: int) -> Device | None:
        for device in self._devices:
            if index in device:
                return device
        return None

    def __getitem__(self, index: int) -> int:
        if 0 <= index <= 0x6FF:
            return self._rom[index]
        elif 0x700 <= index <= 0x7FF:
            device = self._get_device(index)
            if device is not None:
                return device[index]
            else:
                return 0
        elif 0x800 <= index <= 0xFFF:
            return self._ram[index - 0x1000]
        else:
            raise IndexError

    def __setitem__(self, index: int, value: int):
        if 0 <= index <= 0x6FF:
            pass
        elif 0x700 <= index <= 0x7FF:
            device = self._get_device(index)
            if device is not None:
                device[index] = value % MAX_INT
        elif 0x800 <= index <= 0xFFF:
            self._ram[index - 0x1000] = value % MAX_INT
        else:
            raise IndexError

    @staticmethod
    def load_rom_file(file: str | BinaryIO) -> list[int]:
        rom: list[int] = []

        if isinstance(file, str):
            with open(file, 'b') as f:
                while f:
                    incoming = f.read(3)
                    rom.append(incoming[0] << 4 | ((incoming[1] & 0xf0) >> 4))
                    rom.append(((incoming[1] & 0xf) << 8) | incoming[2])
        else:
            while file:
                incoming = file.read(3)
                rom.append(incoming[0] << 4 | ((incoming[1] & 0xf0) >> 4))
                rom.append(((incoming[1] & 0xf) << 8) | incoming[2])

        return rom


class Computer:

    _mem: Memory

    _running: bool
    _halted: bool

    _interrupt_flag: list[int]

    _pc_last: int
    _zero_flag: bool
    _interruptable: bool

    _pc: int
    _sp: int
    _pt: int
    _d0: int
    _d1: int
    _d2: int
    _d3: int

    def __init__(self, mem: Memory):
        self._mem = mem

        self._running = True
        self._halted = False
        self._interrupt_flag = []

        self._pc_last = 0
        self._zero_flag = False
        self._interruptable = False

        self._pc = 0
        self._sp = 0
        self._pt = 0
        self._d0 = 0
        self._d1 = 0
        self._d2 = 0
        self._d3 = 0

    @property
    def running(self) -> bool: return self._running
    @property
    def halted(self) -> bool: return self._halted
    @property
    def active(self) -> bool: return self.running and not self.halted

    @property
    def zero_flag(self) -> bool: return self._zero_flag

    @property
    def program_counter(self) -> int: return self._pc
    @program_counter.setter
    def program_counter(self, value: int):
        self._pc_last = self._pc
        self._pc = value % MAX_INT
    @property
    def stack_pointer(self) -> int: return self._sp
    @stack_pointer.setter
    def stack_pointer(self, value: int): self._sp = value % MAX_INT
    @property
    def pointer(self) -> int: return self._pt
    @pointer.setter
    def pointer(self, value: int): self._pt = value % MAX_INT
    @property
    def data_0(self) -> int: return self._d0
    @data_0.setter
    def data_0(self, value: int): self._d0 = value % MAX_INT
    @property
    def data_1(self) -> int: return self._d1
    @data_1.setter
    def data_1(self, value: int): self._d1 = value % MAX_INT
    @property
    def data_2(self) -> int: return self._d2
    @data_2.setter
    def data_2(self, value: int): self._d2 = value % MAX_INT
    @property
    def data_3(self) -> int: return self._d3
    @data_3.setter
    def data_3(self, value: int): self._d3 = value % MAX_INT

    def get_reg(
        self,
        index: int,
        *,
        strict: bool = True,
    ) -> int:
        if strict and not (0 <= index <= 7): raise IndexError
        else: index %= 8

        return self._get_reg(index)

    def _get_reg(self, index: int) -> int:
        if index == 1: return self._pc
        elif index == 2: return self._sp
        elif index == 3: return self._pt
        elif index == 4: return self._d0
        elif index == 5: return self._d1
        elif index == 6: return self._d2
        elif index == 7: return self._d3
        else: return 0

    def set_reg(
        self,
        index: int,
        value: int,
        *,
        strict: bool = True,
    ):
        if strict and not (0 <= index <= 7): raise IndexError
        else: index %= 8

        value %= MAX_INT

        self._set_reg(index, value)

    def _set_reg(self, index: int, value: int):
        if index == 1: self._pc = value
        elif index == 2: self._sp = value
        elif index == 3: self._pt = value
        elif index == 4: self._d0 = value
        elif index == 5: self._d1 = value
        elif index == 6: self._d2 = value
        elif index == 7: self._d3 = value

    def interrupt(self, index: int):
        self._interrupt_flag.append(index % MAX_INT)

    def step(self):
        instruction = self._mem[self.program_counter]

        if instruction == 0: self.NOP()
        elif instruction == 1: self.HLT()
        elif instruction == 2: self.INT()
        elif instruction == 3: self.BNZ()
        elif instruction == 4: self.BLK()
        elif instruction == 5: self.ENB()
        elif instruction & 0xFF8 == 0x10: self.GLA(instruction & 0x7)
        elif instruction & 0xFF8 == 0x18: self.GET(instruction & 0x7)
        elif instruction & 0xFF8 == 0x20: self.LOD(instruction & 0x7)
        elif instruction & 0xFF8 == 0x28: self.STR(instruction & 0x7)
        elif instruction & 0xFF8 == 0x30: self.PSH(instruction & 0x7)
        elif instruction & 0xFF8 == 0x38: self.POP(instruction & 0x7)
        elif instruction & 0xF80 == 0x80: self.LDI(instruction & 0x7F)
        elif instruction & 0xFC0 == 0x100:
            self.LSH(instruction & 0x38, instruction & 0x7)
        elif instruction & 0xFC0 == 0x140:
            self.RSH(instruction & 0x38, instruction & 0x7)
        elif instruction & 0xFC0 == 0x180:
            self.INC(instruction & 0x38, instruction & 0x7)
        elif instruction & 0xFC0 == 0x1C0:
            self.DEC(instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0x200:
            self.AND(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0x400:
            self.OR(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0x600:
            self.NAD(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0x800:
            self.SUB(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0xA00:
            self.XOR(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0xC00:
            self.NOR(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        elif instruction & 0xE0 == 0xE00:
            self.ADD(instruction & 0x1C, instruction & 0x38, instruction & 0x7)
        else: raise LookupError()

    # === Operations ===

    def NOP(self):
        self.program_counter += 1

    def HLT(self):
        self._halted = True
        self.program_counter += 1

    def INT(self):
        self.interrupt(self.pointer)
        self.program_counter += 1

    def BNZ(self):
        if self.zero_flag:
            self.program_counter = self.pointer
        self.program_counter += 1

    def BLK(self):
        self._interruptable = False
        self.program_counter += 1

    def ENB(self):
        self._interruptable = True
        self.program_counter += 1

    def GLA(self, REG: int):
        self.set_reg(REG, self._pc_last)
        self.program_counter += 1

    def GET(self, REG: int):
        if self._interrupt_flag: self.set_reg(REG, self._interrupt_flag.pop())
        else: self.set_reg(REG, 0)
        self.program_counter += 1

    def LOD(self, REG: int):
        self.set_reg(REG, self._mem[self.pointer])
        self.program_counter += 1

    def STR(self, REG: int):
        self._mem[self.pointer] = self.get_reg(REG)
        self.program_counter += 1

    def PSH(self, REG: int):
        self.set_reg(REG, self._mem[self.stack_pointer])
        self.program_counter += 1

    def POP(self, REG: int):
        self._mem[self.stack_pointer] = self.get_reg(REG)
        self.program_counter += 1

    def LDI(self, Immediate: int):
        self.pointer = Immediate % 0x3F
        self.program_counter += 1

    def LSH(self, REG_D: int, REG_A: int):
        result = self.get_reg(REG_A) << 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def RSH(self, REG_D: int, REG_A: int):
        result = self.get_reg(REG_A) >> 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def INC(self, REG_D: int, REG_A: int):
        result = self.get_reg(REG_A) + 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def DEC(self, REG_D: int, REG_A: int):
        result = self.get_reg(REG_A) - 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def AND(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) & self.get_reg(REG_B)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def OR(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) | self.get_reg(REG_B)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def NAD(self, REG_D: int, REG_A: int, REG_B: int):
        result = (MAX_INT - 1) ^ (self.get_reg(REG_A) & self.get_reg(REG_B))
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def SUB(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) + ((MAX_INT - 1) ^ self.get_reg(REG_B)) + 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def XOR(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) ^ self.get_reg(REG_B)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def NOR(self, REG_D: int, REG_A: int, REG_B: int):
        result = (MAX_INT - 1) ^ (self.get_reg(REG_A) | self.get_reg(REG_B))
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def ADD(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) + self.get_reg(REG_B)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

