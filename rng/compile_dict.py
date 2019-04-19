import json
import time
from collections import defaultdict
from . import metaphone, segmentation


def compile_dmph(segments):
    dmph_dict = defaultdict(list)
    for seg in segments:
        print(seg)
        # This will only be two elements. Secondary will usually be None so we
        # need to filter that out
        for dmph in metaphone.dmetaphone(seg):
            if dmph:
                dmph_dict[dmph].append(seg)
    return dmph_dict


def get_segment_counts(words):
    segment_counts = defaultdict(int)
    for word in words:
        for seg in segmentation.split_segments(word):
            segment_counts[seg] += 1
    return segment_counts


def compile(words):
    segments = get_segment_counts(words)
    dmph = compile_dmph(segments)
    return {"segments": segments, "dmph": dmph}


def compile_from_files(word_file, outfile):
    with open(word_file) as f:
        words = f.read().splitlines()

    # Capitalize all letters
    words = [word.upper() for word in words]

    start_time = time.time()
    output = compile(words)
    elapsed = time.time() - start_time
    print(f"Compiled in {elapsed:.4f}s")

    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Output to {outfile}")
