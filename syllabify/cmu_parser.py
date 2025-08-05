"""
Parses CMU dictionary into Python Dictionary
AC 2017-08-10: updated from Py2 original for Py3
changes other than print() statements noted
"""

import os
import re
import random
import functools

# Settings
CMU_DIR = os.path.join(os.path.dirname(__file__), "CMU_dictionary")
# Version
VERSION = "cmudict.0.7a"
# Path
PATH_TO_DICTIONARY = os.path.join(CMU_DIR, VERSION)

class CMUDictionary:
    """CMU Dictionary parser and interface"""

    def __init__(self, path_to_dictionary=PATH_TO_DICTIONARY):
        self.regexp = re.compile(
            r"""
                        (?P<Comment>;;;.*) # ;;; denotes Comment: to be ignore
                        |(?P<Word>'?\w+[^\(\)]*) # Not interested in first character
                        (?P<Alternative> \(\d+\))? # (digit) denotes that another 
                        (?P<Seperator> \s\s) # Separator: to be ignored
                        (?P<Phoneme> [^\n]+) # The remainder 
                     """,
            re.VERBOSE,
        )

        # import CMU dictionary
        try:
            self.cmudict_file = open(path_to_dictionary, "r", encoding="latin-1")
        except IOError as e:
            print(e, "file not found, check settings...")
            raise
        # create Python CMU dictionary
        self._cmudict = self._create_dictionary()
        self.cmudict_file.close()

    def __getitem__(self, key):
        try:
            return self._cmudict[key.upper()]
        except (KeyError, UnicodeDecodeError):
            return None

    def _create_dictionary(self):
        dict_temp = {}
        for line in self.cmudict_file.readlines():
            match = re.match(self.regexp, line)
            if match:
                dict_temp = self._update_dictionary(match, dict_temp)
        return dict_temp

    def _update_dictionary(self, match, dictionary):
        if match.group("Word") is None:
            # No word found, do nothing
            return dictionary

        if match.group("Word") and (match.group("Alternative") is None):
            # This is a new word
            # Create an entry, and instantiate a Transcription object
            dictionary[match.group("Word")] = Transcription(match.group("Phoneme"))
            return dictionary

        if match.group("Word") and match.group("Alternative"):
            # There is an alternative phoneme representation of the matched word
            # Append phoneme rep. to dictionary entry for this word
            dictionary[match.group("Word")].append(match.group("Phoneme"))
            return dictionary

        return dictionary


class Transcription:
    """the phoneme transcription of the word"""

    def __init__(self, phoneme):
        self.representation = [Phoneme(phoneme)]

    def __len__(self):
        return len(self.representation)

    def __str__(self):
        return (
            "["
            + functools.reduce(
                lambda x, y: str(x) + str(y) + ", ", self.representation, ""
            )
            + "]"
        )

    def append(self, phoneme):
        self.representation.append(Phoneme(phoneme))

    def get_phonemic_representations(self):
        # return all the phonemes that can represent this word
        return [x.phoneme for x in self.representation]


class Phoneme:
    """Individual phoneme representation"""

    def __init__(self, phoneme):
        self.phoneme = phoneme

    def __str__(self):
        return str(self.phoneme)


# create dictionary
cmudict = CMUDictionary()


def CMUtranscribe(word):
    """Transcribe a word using CMU dictionary"""
    try:
        transcription = cmudict[word]
        if transcription:
            return transcription.get_phonemic_representations()
        return None
    except AttributeError:
        # Entry not found
        return None


def test_word(word):
    """Test function for a single word"""
    return CMUtranscribe(word)


def test():
    """Test Function - prints the transcription of 100 words"""
    try:
        with open("./CMU_dictionary/american-english", "r") as words_file:
            words = words_file.readlines()
    except FileNotFoundError:
        print("american-english file not found, using sample words")
        words = ["hello\n", "world\n", "python\n", "linguistics\n"]

    for i in range(min(100, len(words))):
        word = random.choice(words)[:-1]
        syllable = CMUtranscribe(word)
        if syllable:
            transcriptions = 0
            output = word
            for ph in syllable:
                transcriptions += 1
                output += "\n"
                output += str(transcriptions) + (": " + ph)
            output += "\n"
            print(output)


if __name__ == "__main__":
    test()
