# Kyler Olsen
# Feb 2024

MAX_INT = 4089


class Memory:

    def __getitem__(self, index: int) -> int:
        return 0

    def __setitem__(self, index: int, value: int):
        pass


class Computer:

    _mem: Memory

    _running: bool
    _halted: bool

    _zero_flag: bool
    _interrupt_flag: list[int]

    _pc: int
    _sp: int
    _pt: int
    _d0: int
    _d1: int
    _d2: int
    _d3: int

    _interrupt_map: list[int]

    def __init__(self, mem: Memory):
        self._mem = mem

        self._running = True
        self._halted = False
        self._zero_flag = False
        self._interrupt_flag = []

        self._pc = 0
        self._sp = 0
        self._pt = 0
        self._d0 = 0
        self._d1 = 0
        self._d2 = 0
        self._d3 = 0

        self._interrupt_map = [0] * MAX_INT

    @property
    def running(self) -> bool: return self._running
    @property
    def halted(self) -> bool: return self._halted
    @property
    def active(self) -> bool: return self.running and self.halted

    @property
    def zero_flag(self) -> bool: return self._zero_flag

    @property
    def program_counter(self) -> int: return self._pc
    @program_counter.setter
    def program_counter(self, value: int): self._pc = value % MAX_INT
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
        top: bool = False,
        strict: bool = False,
    ) -> int:
        if strict and not (0 <= index <= 7): raise IndexError
        elif strict and top and not (0 <= index <= 3): raise IndexError
        elif top and not (0 <= index <= 3): index = (index % 4) + 4
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
        top: bool = False,
        strict: bool = False,
    ):
        if strict and not (0 <= index <= 7): raise IndexError
        elif strict and top and not (0 <= index <= 3): raise IndexError
        elif top and not (0 <= index <= 3): index = (index % 4) + 4
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

    # === Operations ===

    def NOP(self):
        self.program_counter += 1

    def HLT(self):
        self._halted = True
        self.program_counter += 1

    def INT(self):
        self.interrupt(self.pointer)
        self.program_counter += 1

    def JPZ(self):
        if self.zero_flag:
            self.program_counter = self.pointer
        self.program_counter += 1

    def SET(self, REG: int):
        self._interrupt_map[self.pointer] = self.get_reg(REG, top=True)
        self.program_counter += 1

    def LOD(self, REG: int):
        self.set_reg(REG, self._mem[self.pointer], top=True)
        self.program_counter += 1

    def STR(self, REG: int):
        self._mem[self.pointer] = self.get_reg(REG, top=True)
        self.program_counter += 1

    def PSH(self, REG: int):
        self.set_reg(REG, self._mem[self.stack_pointer])
        self.program_counter += 1

    def POP(self, REG: int):
        self._mem[self.stack_pointer] = self.get_reg(REG)
        self.program_counter += 1

    def LSH(self, REG_D: int, REG_A: int):
        result = self.get_reg(REG_A) << 1
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result, top=True)
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
        result = self.get_reg(REG_A) & self.get_reg(REG_B, top=True)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result, top=True)
        self.program_counter += 1

    def XOR(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) ^ self.get_reg(REG_B, top=True)
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result, top=True)
        self.program_counter += 1

    def NOR(self, REG_D: int, REG_A: int, REG_B: int):
        result = MAX_INT ^ (self.get_reg(REG_A) | self.get_reg(REG_B))
        result %= MAX_INT
        self._zero_flag = result == 0
        self.set_reg(REG_D, result)
        self.program_counter += 1

    def SUB(self, REG_D: int, REG_A: int, REG_B: int):
        result = self.get_reg(REG_A) - self.get_reg(REG_B)
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

    def LDI(self, REG: int, Immediate: int):
        self.set_reg(REG, Immediate)
        self.program_counter += 1

