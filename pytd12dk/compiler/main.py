# Kyler Olsen
# Feb 2024

from typing import Sequence
import argparse

def compile(args: argparse.Namespace):
    pass

def parser(parser: argparse.ArgumentParser):
    parser.set_defaults(func=compile)

def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        description='ytd 12-bit Computer Compiler',
    )

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
