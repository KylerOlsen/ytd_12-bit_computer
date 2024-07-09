# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .assembler import Program, INSTRUCTIONS_COUNT

def assemble(args: argparse.Namespace):

    program = Program(args.input_file.read())

    try: assert len(bytes(program)) <= INSTRUCTIONS_COUNT * 1.5
    except AssertionError:
        print(
            hex(int(len(bytes(program)) / 1.5)),
            '>',
            hex(INSTRUCTIONS_COUNT),
            ':',
            hex(int(len(bytes(program)) / 1.5) - INSTRUCTIONS_COUNT),
        )
        raise

    if args.output_file:
        args.output_file.write(bytes(program))

    if args.labels_file:
        for label, location in program.labels().items():
            args.labels_file.write(f"{hex(location)}, {label}\n")

    if args.hex_file:
        args.hex_file.write(program.hex_str())

def parser(parser: argparse.ArgumentParser):
    parser.add_argument('input_file', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output_file', type=argparse.FileType('wb'))
    parser.add_argument('-l', '--labels_file', type=argparse.FileType('w'))
    parser.add_argument('-x', '--hex_file', type=argparse.FileType('w'))
    parser.set_defaults(func=assemble)

def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Linker and Assembler',
        epilog='https://github.com/KylerOlsen/ytd_12-bit_computer',
    )

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
