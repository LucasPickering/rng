import json
import time
from . import metaphone
from collections import defaultdict, Counter


def compile_from_files(infile, outfile):
    with open(infile) as f:
        words = f.read().splitlines()

    start_time = time.time()
    dmph_dict = compile(words)
    elapsed = time.time() - start_time
    print(f"Compiled in {elapsed:.4f}s")

    with open(outfile, "w") as f:
        json.dump(dmph_dict, f, indent=2)


def compile(words):
    dmph_word_segments = [metaphone.dmetaphone_segments(word) for word in words]

    dmph_to_segment = defaultdict(Counter)
    for word_segments in dmph_word_segments:
        for segment, dmphs in word_segments:
            for dmph in dmphs:
                if dmph:
                    dmph_to_segment[dmph].update(segment)

    return dmph_to_segment
