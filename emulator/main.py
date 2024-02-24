# Kyler Olsen
# Feb 2024

from typing import Sequence

from .emulator import Computer, Memory
from .devices import tty


def simple_computer_with_tty(rom: list[int]) -> Computer:
    return Computer(Memory(rom, [tty(0x7FE, 0x7FF)]))

def main(argv: Sequence[str]):
    import argparse

    machines = {
        'tty': simple_computer_with_tty
    }

    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Emulator',
    )
    parser.add_argument('rom_file', type=argparse.FileType('rb'))
    parser.add_argument(
        '-m', '--machine', choices=machines.keys(), default='tty')

    args = parser.parse_args(argv)

    computer = machines[args.machine](Memory.load_rom_file(args.rom_file))

    while computer.active:
        computer.step()

if __name__ == '__main__':
    from sys import argv
    main(argv)
