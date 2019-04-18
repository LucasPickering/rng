import argparse
from . import compile_dict
from .rng import RNG


def compile(args):
    compile_dict.compile_from_files(args.mode, args.word_list, args.output)


def gen(args):
    rng = RNG(args.dmph_dict, args.vowel_dict)
    source = " ".join(args.source)
    result = rng.generate(source)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="rng", description="Random name generator"
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    parser_compile = subparsers.add_parser(
        "compile", help="Compile the dictionary"
    )
    parser_compile.add_argument("mode", choices=compile_dict.MODES.keys())
    parser_compile.add_argument(
        "--word-list", "-w", default="english-words/words_alpha.txt"
    )
    parser_compile.add_argument("--output", "-o", default="output.json")
    parser_compile.set_defaults(func=compile)

    parser_gen_name = subparsers.add_parser("gen", help="Generate names")
    parser_gen_name.add_argument("source", nargs="+", help="The source name")
    parser_gen_name.add_argument("--dmph-dict", "-d", default="dmph_dict.json")
    parser_gen_name.add_argument(
        "--vowel-dict", "-v", default="vowel_dict.json"
    )
    parser_gen_name.set_defaults(func=gen)

    args = parser.parse_args()
    args.func(args)
