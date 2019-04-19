import json
import random
from collections import defaultdict
from . import metaphone, segmentation


class DataContainer:
    """
    Computes then stores some useful data dumps.
    """

    def __init__(self, data_dict):
        self._segment_freqs = data_dict["segments"]
        self._dmph_lookup = data_dict["dmph"]

        # Group vowel segments by length
        self._vowel_segments_by_len = defaultdict(dict)
        for seg, freq in self._segment_freqs.items():
            if segmentation.is_vowel_segment(seg):
                self._vowel_segments_by_len[len(seg)].update({seg: freq})

    @property
    def segment_freqs(self):
        return self._segment_freqs

    @property
    def dmph_lookup(self):
        return self._dmph_lookup

    @property
    def vowel_segments_by_len(self):
        return self._vowel_segments_by_len


class Randomizer:
    """
    A utility for generating randomness.
    """

    def weighted_choice(self, weighted_dict):
        vals, weights = zip(*weighted_dict.items())
        return random.choices(vals, weights, k=1)[0]


class TokenBuilder:
    """
    A builder for one token in a name randomization. This stores some interval
    state, and has a set of external methods for applying different mutations
    to the state. Once you're done mutating, you call .build() to get a name.

    Right now this is only meant to operate on one token (i.e. one word)
    """

    def __init__(self, data_container, randomizer, source, init=True):
        self._data_container = data_container
        self._randomizer = randomizer
        # Our original copies, that shouldn't be mutated
        self._source = source.upper()
        self._source_segments = segmentation.split_segments(self._source)

        # Our working copies that will be mutated
        if init:
            self._build_caches()

    def _build_caches(self):
        # Shallow copy
        self._segments = list(self._source_segments)

    def randomize_dmph(self):
        # For each segment, DMPH it, then pick a random other segment that
        # DMPHs to the same thing
        for i, segment in enumerate(self._segments):
            if segmentation.is_consonant_segment(segment):
                prim, _ = metaphone.dmetaphone(segment)
                weighted_dmphs = {
                    seg: self._data_container.segment_freqs[seg]
                    for seg in self._data_container.dmph_lookup[prim]
                }
                self._segments[i] = self._randomizer.weighted_choice(
                    weighted_dmphs
                )
        return self

    def randomize_vowels(self):
        # Randomize all the vowel segments
        for i, segment in enumerate(self._segments):
            if segmentation.is_vowel_segment(segment):
                # TODO handle if the segment length isn't in the dict
                self._segments[i] = self._randomizer.weighted_choice(
                    self._data_container.vowel_segments_by_len[len(segment)]
                )
        return self

    def reset(self):
        """
        Resets the internal state of this builder
        """
        self._build_caches()
        return self

    def build(self):
        return "".join(self._segments).capitalize()


class RNG:
    def __init__(self, dict_file):
        with open(dict_file) as f:
            d = json.load(f)
        self._data_container = DataContainer(d)
        self._randomizer = Randomizer()

    def generate(self, source, iterations=1):
        # Make all caps and split on whitespace
        source_tokens = source.upper().split()
        builders = [
            TokenBuilder(
                self._data_container, self._randomizer, token, init=False
            )
            for token in source_tokens
        ]

        # Run n iterations
        return [
            # Join the tokens with spaces
            " ".join(
                # Build a random token for each token in the source string
                builder.reset().randomize_vowels().randomize_dmph().build()
                for builder in builders
            )
            for _ in range(iterations)
        ]

