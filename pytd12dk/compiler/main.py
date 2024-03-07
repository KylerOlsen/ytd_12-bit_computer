# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .compiler_types import CompilerError
from .lexer import lexer, LexerError
from .syntactical_analyzer import syntactical_analyzer, SyntaxError


def _compile(args: argparse.Namespace):
    tokens = lexer(args.input_file.read(), args.input_file.name)

    if args.token_file:
        for token in tokens:
            args.token_file.write(str(token) + "\n")

    syntax = syntactical_analyzer(tokens)

    if args.syntax_file:
        args.syntax_file.write(syntax.tree_str())

def compile(args: argparse.Namespace):
    try: _compile(args)
    except CompilerError as e: print(e.compiler_error())
    except Exception as e:
        raise Exception(
            "You found an error in the compiler!\n"
            "\tPlease report this issue on Github:\n"
            "\thttps://github.com/KylerOlsen/ytd_12-bit_computer/issues"
        ) from e

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
