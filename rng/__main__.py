import argparse
from . import gen_dict
from .rng import RNG


# _ACTIONS = {"gendict": gen_dict.generate_from_files}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('action')
    # parser.add_argument(
    #     "--input", "-i", default="english-words/words_alpha.txt"
    # )
    # parser.add_argument("--output", "-o", default="dmph_dict.json")
    parser.add_argument("source")
    parser.add_argument("--dict", "-d", default="dmph_dict.json")
    args = parser.parse_args()

    # gen_dict.generate_from_files(args.input, args.output)
    rng = RNG(args.dict)
    print(rng.generate(args.source))
