# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

from .compiler_types import CompilerError
from .lexer import lexer
from .syntactical_analyzer import syntactical_analyzer
from .semantical_analyzer import semantical_analyzer
from .code_generator import code_generator

def _compile(args: argparse.Namespace):
    tokens = lexer(args.input_file.read(), args.input_file.name)

    if args.token_file:
        for token in tokens:
            args.token_file.write(str(token) + "\n")

    syntax_tree = syntactical_analyzer(tokens)

    if args.syntax_file:
        args.syntax_file.write(syntax_tree.tree_str())

    annotated_syntax_tree = semantical_analyzer(syntax_tree)

    if args.annotated_file:
        args.annotated_file.write(annotated_syntax_tree.tree_str())

    assembly_code = code_generator(annotated_syntax_tree)

    if args.assembly_file:
        args.assembly_file.write(assembly_code)

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
    parser.add_argument('-o', '--output_file', type=argparse.FileType('wb'))
    parser.add_argument(
        '-t', '--token_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.add_argument(
        '-x', '--syntax_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.add_argument(
        '-n', '--annotated_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.add_argument(
        '-a', '--assembly_file', type=argparse.FileType('w', encoding='utf-8'))
    parser.set_defaults(func=compile)

def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Compiler',
        epilog='https://github.com/KylerOlsen/ytd_12-bit_computer',
    )

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
