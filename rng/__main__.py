import argparse
from . import compile_dict
from .rng import RNG

DEFAULT_DICT_FILE = "dictionary.json"


def compile(args):
    compile_dict.compile_from_files(args.word_list, args.output)


def gen(args):
    rng = RNG(args.dict)
    source = " ".join(args.source)
    result = rng.generate(source, args.iterations)
    for name in result:
        print(name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="rng", description="Random name generator"
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    parser_compile = subparsers.add_parser(
        "compile", help="Compile the dictionary"
    )
    parser_compile.add_argument(
        "--word-list", "-w", default="english-words/words_alpha.txt"
    )
    parser_compile.add_argument("--output", "-o", default=DEFAULT_DICT_FILE)
    parser_compile.set_defaults(func=compile)

    parser_gen_name = subparsers.add_parser("gen", help="Generate names")
    parser_gen_name.add_argument("source", nargs="+", help="The source name")
    parser_gen_name.add_argument("--dict", "-d", default=DEFAULT_DICT_FILE)
    parser_gen_name.add_argument("--iterations", "-i", type=int, default=5)
    parser_gen_name.set_defaults(func=gen)

    args = parser.parse_args()
    args.func(args)
