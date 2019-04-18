from collections import Counter

VOWELS = {"a", "e", "i", "o", "u"}


def is_vowel(char):
    # Ignore y as a vowel
    return char in VOWELS


def is_vowel_segment(segment):
    return is_vowel(segment[0])


def split_segments(word):
    """
    Splits a word into a series of vowel/consonant segments, e.g.
    "shear" -> ["sh", "ea", "r"]
    """

    segments = []
    current_segment = (0, False)  # Start index, is_vowel

    # Scan the word for vowel segments
    for i, char in enumerate(word):
        vowel = is_vowel(char)
        if i == 0:
            current_segment = (i, vowel)
        elif vowel != current_segment[1]:
            # The segment type has changed
            # Save the segment and start a new one
            segments.append(word[current_segment[0] : i])
            current_segment = (i, vowel)
    # Save the last segment
    segments.append(word[current_segment[0] :])
    return segments


def get_vowel_segments(words):
    """
    Get a dict of vowel n-grams to counts, e.g.
    {
        "a": 13,
        "ea": 35,
        "oo": 19,
        ...
    }
    """
    vowel_segments = []
    for word in words:
        vowel_segments.extend(
            seg for seg in split_segments(word) if is_vowel_segment(seg)
        )

    return Counter(vowel_segments)
