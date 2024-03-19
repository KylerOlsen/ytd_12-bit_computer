# Kyler Olsen
# Feb 2024

from .emulator import Device


try:
    # Windows
    import msvcrt
    def getch() -> int:
        return msvcrt.getch()[0]
except ImportError:
    # Unix
    import sys
    import tty, termios
    def getch() -> int:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1).encode('utf-8')[0]
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class tty(Device):

    def __getitem__(self, index: int) -> int:
        if index & 0xf == 0xd: return 0
        elif index & 0xf == 0xe: return 0
        elif index & 0xf == 0xf: return getch()
        else: return 0

    def __setitem__(self, index: int, value: int):
        if index & 0xf == 0xd:
            if value & 0x800:
                print((((value & 0x7FF) ^ 0x7FF) + 1) * -1)
            else:
                print(value)
        elif index & 0xf == 0xe:
            print(value)
        elif index & 0xf == 0xf:
            print(chr(value & 0x7f), end='')
