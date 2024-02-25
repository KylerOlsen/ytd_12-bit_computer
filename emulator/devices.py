# Kyler Olsen
# Feb 2024

from .emulator import Device


class tty(Device):

    def __setitem__(self, index: int, value: int):
        if index & 0xf == 0xd:
            if value & 0x800:
                print((((value & 0x7FF) ^ 0x7FF) + 1) * -1)
            else:
                print(value)
        elif index & 0xf == 0xe:
            print(value)
        elif index & 0xf == 0xf:
            print(chr(value), end='')
