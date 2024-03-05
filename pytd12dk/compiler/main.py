# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .lexer import lexer
from .syntactical_analyzer import syntactical_analyzer

def compile(args: argparse.Namespace):
    tokens = lexer(args.input_file.read(), args.input_file.name)

    if args.token_file:
        for token in tokens:
            args.token_file.write(str(token) + "\n")

    syntax = syntactical_analyzer(tokens)

    if args.syntax_file:
        args.syntax_file.write(syntax.tree_str())

def parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        'input_file', type=argparse.FileType('r', encoding='utf-8'))
    # parser.add_argument('-o', '--output_file', type=argparse.FileType('wb'))
    parser.add_argument(
        '-t', '--token_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.add_argument(
        '-x', '--syntax_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.set_defaults(func=compile)

def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Compiler',
    )

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
