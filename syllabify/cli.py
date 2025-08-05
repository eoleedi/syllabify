"""
Command Line Interface for syllabify
"""

import sys
from .syllable import generate_sentence


def main():
    """Main function for command line usage"""
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        syllables = generate_sentence(" ".join(words))
        for syllable in syllables:
            print(syllable)  # print syllables
    else:
        print(
            "Please input a word, or list of words (space-separated) as argument variables"
        )
        print("e.g. syllabify linguistics phonetics")


if __name__ == "__main__":
    main()
