VOWELS = ["a", "e", "i", "o", "u", "y"]


# https://stackoverflow.com/a/5615724
def split_syllables(word):
    num_vowels = 0
    last_was_vowel = False
    for char in word:
        found_vowel = False
        if char in VOWELS:
            # don't count consecutive vowels
            if last_was_vowel:
                found_vowel = True
            else:
                num_vowels += 1
                found_vowel = False
            last_was_vowel = True

        # if full cycle and no vowel found, set lastWasVowel to false;
        if not found_vowel:
            last_was_vowel = False

    # remove silent e or es
    if (len(word) > 1 and word[-1] == "e") or (
        len(word) > 2 and word[-2:] == "es"
    ):
        num_vowels -= 1

    return num_vowels
