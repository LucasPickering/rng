import json
import time
from collections import defaultdict, Counter
from . import metaphone, vowels


def compile_dmph(words):
    dmph_word_segments = [metaphone.dmetaphone_segments(word) for word in words]

    dmph_to_segment = defaultdict(Counter)
    for word_segments in dmph_word_segments:
        for segment, dmphs in word_segments:
            for dmph in dmphs:
                if dmph:
                    dmph_to_segment[dmph].update(segment)

    return dmph_to_segment


def compile_vowels(words):
    return vowels.get_vowel_segments(words)


MODES = {"dmph": compile_dmph, "vowels": compile_vowels}


def compile_from_files(mode, word_file, outfile):
    with open(word_file) as f:
        words = f.read().splitlines()

    compiler = MODES[mode]

    start_time = time.time()
    output = compiler(words)
    elapsed = time.time() - start_time
    print(f"Compiled in {elapsed:.4f}s")

    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)
