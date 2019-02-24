import json
import random
from . import metaphone


class RNG:
    def __init__(self, dmph_dict_file):
        with open(dmph_dict_file) as f:
            self._dmph_dict = json.load(f)

    def generate(self, source):
        source_segment_dmphs = metaphone.dmetaphone_segments(source)
        dmphs = (prim for seg, (prim, sec) in source_segment_dmphs)
        random_segs = (
            random.choice(list(self._dmph_dict[dmph].keys()))
            for dmph in dmphs
            if dmph
        )
        return "".join(random_segs).capitalize()
