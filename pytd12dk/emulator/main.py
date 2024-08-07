# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .emulator import Computer, Memory
from .devices import tty

MACHINES = {
    'tty': lambda rom: Computer(Memory(rom, [tty(0x7FD, 0x7FF)]))
}

def emulate(args: argparse.Namespace):
    from time import sleep

    computer = MACHINES[args.machine](Memory.load_rom_file(args.rom_file))

    try:
        while computer.active:
            if args.verbose:
                print(
                    f"ZR: {hex(0)} \t"
                    f"PC: {hex(computer.program_counter)} \t"
                    f"SP: {hex(computer.stack_pointer)} \t"
                    f"MP: {hex(computer.pointer)}"
                )
                print(
                    f"D0: {hex(computer.data_0)} \t"
                    f"D1: {hex(computer.data_1)} \t"
                    f"D2: {hex(computer.data_2)} \t"
                    f"D3: {hex(computer.data_3)}"
                )
            if args.step:
                input("Press enter to step to next instruction...")
            computer.step(args.verbose)
            if not args.step:
                sleep(int(args.clock)/1000)
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Program Exiting...")

def parser(parser: argparse.ArgumentParser):
    parser.add_argument('rom_file', type=argparse.FileType('rb'))
    parser.add_argument(
        '-m', '--machine', choices=MACHINES.keys(), default='tty')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--step', action='store_true')
    parser.add_argument('-c', '--clock', default='100')
    parser.set_defaults(func=emulate)

def main(argv: Sequence[str] | None = None):

    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Emulator',
        epilog='https://github.com/KylerOlsen/ytd_12-bit_computer',
    )
    parser.add_argument('rom_file', type=argparse.FileType('rb'))
    parser.add_argument(
        '-m', '--machine', choices=MACHINES.keys(), default='tty')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--step', action='store_true')
    parser.add_argument('-c', '--clock', default='100')

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
