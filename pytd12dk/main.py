# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .emulator.main import parser as emulator_parser
from .compiler.main import parser as compiler_parser
from .assembler.main import parser as assembler_parser

def main(argv: Sequence[str] | None = None):

    parser = argparse.ArgumentParser(
        description='ytd 12-bit Development Kit',
    )

    subparsers = parser.add_subparsers(required=True)

    parser_emulator = subparsers.add_parser('em', help='Emulator help')
    emulator_parser(parser_emulator)

    parser_compiler = subparsers.add_parser('cm', help='Compiler help')
    compiler_parser(parser_compiler)

    parser_assembler = subparsers.add_parser('am', help='Assembler help')
    assembler_parser(parser_assembler)

    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    main()
