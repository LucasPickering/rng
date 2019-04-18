import json
import random
from collections import defaultdict
from . import metaphone, vowels


def weighted_choice(weighted_dict):
    # TODO: make this weighted
    return random.choice(list(weighted_dict.keys()))


class NameBuilder:
    """
    A builder for name randomization. This stores some interval state, and has
    a set of external methods for applying different mutations to the state.
    Once you're done mutating, you call .build() to get a name.

    Right now this is only meant to operate on one token (i.e. one word)
    """

    def __init__(self, source):
        self._source = source
        # Build caches for different generation techniques
        self._segments = vowels.split_segments(source)
        self._dmph_segments = metaphone.dmetaphone_segments(source)
        print(self._dmph_segments)

    def generate_dmph(self, dmph_dict):
        # TODO make this work
        dmphs = (prim for seg, (prim, sec) in self._dmph_segments)
        random_segs = (
            weighted_choice(dmph_dict[dmph]) for dmph in dmphs if dmph
        )
        return "".join(random_segs).capitalize()

    def randomize_vowels(self, vowel_dict):
        # Randomize all the vowel segments
        for i, segment in enumerate(self._segments):
            if vowels.is_vowel_segment(segment):
                # TODO handle if the segment length isn't in the dict
                self._segments[i] = weighted_choice(vowel_dict[len(segment)])
        return self

    def build(self):
        return "".join(self._segments).capitalize()


class RNG:
    def __init__(self, dmph_dict_file, vowel_dict_file):
        with open(dmph_dict_file) as f:
            self._dmph_dict = json.load(f)

        with open(vowel_dict_file) as f:
            vowel_dict = json.load(f)
        # Group vowel segments by length
        self._vowel_dict = defaultdict(dict)
        for seg, freq in vowel_dict.items():
            self._vowel_dict[len(seg)].update({seg: freq})

    def generate(self, source):
        source_tokens = source.split()  # Split on whitespace
        return (
            NameBuilder(source_tokens[0])
            .randomize_vowels(self._vowel_dict)
            .build()
        )
